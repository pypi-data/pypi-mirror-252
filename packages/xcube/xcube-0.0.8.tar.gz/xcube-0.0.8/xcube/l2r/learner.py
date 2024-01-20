# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/09_l2r.learner.ipynb.

# %% auto 0
__all__ = ['SkipToEpoch', 'L2RLearner', 'get_learner']

# %% ../../nbs/09_l2r.learner.ipynb 2
from fastai.torch_imports import *
from fastai.learner import *
from fastai.optimizer import *
from fastai.torch_core import *
from fastcore.all import *
from ..imports import *
from ..metrics import *
from .gradients import *

# %% ../../nbs/09_l2r.learner.ipynb 6
from fastai.callback.core import *

# %% ../../nbs/09_l2r.learner.ipynb 7
class SkipToEpoch(Callback):
    "Skip training up to `epoch`"
    order = 70
    
    def __init__(self, epoch:int):
        self._skip_to = epoch

    def before_epoch(self):
        if self.epoch < self._skip_to:
            raise CancelEpochException
    
    def after_cancel_epoch(self): pass

# %% ../../nbs/09_l2r.learner.ipynb 8
class L2RLearner:
    def __init__(self, 
        model, 
        dls, 
        grad_func, 
        loss_func, 
        lr, 
        cbs, 
        opt_func=SGD, 
        path=None,
        model_dir:str|Path='models', # Subdirectory to save and load models
        moms:tuple=(0.95,0.08,0.95)
    ):
        store_attr(but='cbs')
        self.path = Path(path) if path is not None else getattr(dls, 'path', Path('.'))
        self.cbs = L()
        self.add_cbs(cbs)
        self.logger = print

    def add_cb(self, cb):
        cb.learn = self
        setattr(self, cb.name, cb)
        self.cbs.append(cb)
        return self

    def add_cbs(self, cbs):
        L(cbs).map(self.add_cb)
        return self
    
    @contextmanager
    def added_cbs(self, cbs):
        self.add_cbs(cbs)
        try: yield
        finally: self.remove_cbs(cbs)
        
    @contextmanager
    def removed_cbs(self, cbs):
        self.remove_cbs(cbs)
        try: yield self
        finally: self.add_cbs(cbs)
        
    def remove_cbs(self, cbs):
        L(cbs).map(self.remove_cb)
        return self
    
    def remove_cb(self, cb):
        cb.learn = None
        if hasattr(self, cb.name): delattr(self, cb.name)
        if cb in self.cbs: self.cbs.remove(cb)
        return self

    def _step(self): self.opt.step()
        
    def one_batch(self, *args, **kwargs):
        # self('before_batch')
        self.preds = self.model(self.xb)
        self('after_pred')
        # if self.model.training: # training
        if not self.model.training: return
        self.srtd_preds, self.lambda_i = self.grad_func(self.preds, self.xb)
        self.lambda_i = self.lambda_i.half()
        self('after_loss')
        self('before_backward')
        self.srtd_preds.backward(self.lambda_i)
        self('after_backward')
        
        # free memory (TODO: Put this in a little callback)
        self.lambda_i = None
        import gc; gc.collect()
        torch.cuda.empty_cache()
            
        # self('before_step')
        # self.opt.step()
        self._with_events(self._step, 'step', CancelStepException)
        # self('after_step')
        self.opt.zero_grad()
            
        # self('after_batch')
        
    def one_epoch(self, train, **kwargs):
        self.model.training = train
        self.dl = self.dls.train if train else self.dls.valid
        (self._do_epoch_validate, self._do_epoch_train)[self.model.training](**kwargs)
        
    def _do_epoch_train(self, *args, **kwargs):
        self._with_events(partial(self._all_batches, *args, **kwargs), 'train', CancelTrainException)
        # self('before_train')
        # self._all_batches(*args, **kwargs)
        # self('after_train')
        
    def _do_epoch_validate(self, *args, idx=1, dl=None, **kwargs):
        if dl is None: dl = self.dls[idx]
        self.dl = dl
        with torch.no_grad():
            self._with_events(partial(self._all_batches, *args, **kwargs), 'validate', CancelValidException)
            # self('before_validate')
            # self._all_batches(*args, **kwargs)
            # self('after_validate')
        
    def _all_batches(self, *args, **kwargs):
        self.n_iter = len(self.dl)
        for self.iter_num, self.xb in enumerate(self.dl):
            self._with_events(partial(self.one_batch, *args, **kwargs), 'batch', CancelBatchException)
    
    def create_opt(self):
        self.opt = self.opt_func(self.model.parameters(), self.lr)
        # self.opt.clear_state()
        return self.opt
    
    def _do_epoch(self, **kwargs):
        self.one_epoch(True, **kwargs)
        self.one_epoch(False, **kwargs)

    def fit(self, n_epochs, cbs=None, start_epoch=0, lr=None, wd=None, reset_opt=False, **kwargs):
        if start_epoch != 0:
            cbs = L(cbs) + SkipToEpoch(start_epoch)
        with self.added_cbs(cbs):
            opt = getattr(self, 'opt', None)
            if opt is None or reset_opt: self.create_opt()
            if wd is not None: self.opt.set_hypers(wd=wd)
            self.opt.set_hypers(lr=self.lr if lr is None else lr)
            self.n_epochs = n_epochs
            self('before_fit')
            try:
                for self.epoch,_ in enumerate(range(self.n_epochs)):
                    self._with_events(partial(self._do_epoch, **kwargs), 'epoch', CancelEpochException)
                    # self('before_epoch')
                    # self.one_epoch(True, **kwargs)
                    # self.one_epoch(False, **kwargs)
                    # self('after_epoch')
            except CancelFitException: pass 
            self('after_fit')
    
    def validate(self, idx=1, dl=None, **kwargs):
        try: 
            self.model.training = False
            self._do_epoch_validate(idx, dl, **kwargs)
        except CancelFitException: pass
    
    def __call__(self, name):
        for cb in self.cbs: getattr(cb, name, noop)()
        
    def _with_events(self, f, event_type, ex, final=noop):
        try: self(f'before_{event_type}'); f()
        except ex: self(f'after_cancel_{event_type}')
        self(f'after_{event_type}'); final()
        

# %% ../../nbs/09_l2r.learner.ipynb 10
@patch
@delegates(save_model)
def save(self:L2RLearner, file, **kwargs):
    "Save model and optimizer state (if 'with_opt') to `self.path/file`"
    file = join_path_file(file, self.path/self.model_dir, ext='.pth')
    save_model(file, self.model, getattr(self, 'opt', None), **kwargs)
    return file

# %% ../../nbs/09_l2r.learner.ipynb 11
@patch
@delegates(load_model)
def load(self:L2RLearner, file, device=None, **kwargs):
    "Load model and optimizer state (if `with_opt`) from `self.path/file` using `device`"
    if device is None and hasattr(self.dls, 'device'): device = self.dls.device
    self.opt = getattr(self, 'opt', None)
    if self.opt is None: self.create_opt()
    file = join_path_file(file, self.path/self.model_dir, ext='.pth')
    load_model(file, self.model, self.opt, device=device, **kwargs)
    return self

# %% ../../nbs/09_l2r.learner.ipynb 12
@patch
def show_results(self:L2RLearner, device=None, k=None):
    "Produces the ranking for 100 random labels"
    dataset = to_device(self.dls.train.dataset, device=device)
    num_lbs = dataset.shape[0]
    idxs = torch.randperm(num_lbs)[:100]
    xb = dataset[idxs]
    xb = xb.unsqueeze(0)
    preds, preds_rank, *_,  _ndcg_at_k = ndcg(self.model(xb), xb, k=k)
    if _ndcg_at_k is not None: _ndcg_at_k.squeeze_(0) 
    # lbs = xb[:, :, :, 1].unique().cpu().numpy()
    lbs = idxs.numpy()
    cols = pd.MultiIndex.from_product([lbs, ('tok', 'lbl', 'rank', 'score', 'preds', 'model_rank')], names=['label', 'key2'])
    data = torch.concat( (xb, preds.unsqueeze(-1), preds_rank.unsqueeze(-1)), dim=-1).squeeze(0).permute(1, 0, 2).contiguous()
    data = data.reshape(data.shape[0], -1)
    df_results = pd.DataFrame(data, columns=cols)
    df_results.index.name = 'toks'
    # pd.set_option('display.max_columns', None)
    df_ndcg = pd.DataFrame({'labels': lbs, 'ndcg_at_k':_ndcg_at_k.cpu().numpy()})
    return df_results, df_ndcg

# %% ../../nbs/09_l2r.learner.ipynb 14
def get_learner(model, dls, grad_fn=rank_loss3, loss_fn=loss_fn2, lr=1e-5, cbs=None, opt_func=partial(SGD, mom=0.9), lambrank=False, **kwargs):
    if lambrank: grad_fn = partial(grad_fn, lambrank=lambrank)
    learner = L2RLearner(model, dls, grad_fn, loss_fn, lr, cbs, opt_func=opt_func, **kwargs)
    return learner
