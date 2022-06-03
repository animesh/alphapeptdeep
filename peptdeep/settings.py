# AUTOGENERATED! DO NOT EDIT! File to edit: nbdev_nbs/settings.ipynb (unless otherwise specified).

__all__ = ['update_settings', 'update_modifications', 'global_settings', 'model_const']

# Cell
import os
import collections

from alphabase.yaml_utils import load_yaml
from alphabase.constants.modification import (
    load_mod_df, _keep_only_important_modloss
)

_base_dir = os.path.dirname(__file__)

global_settings = load_yaml(
    os.path.join(_base_dir, 'constants/default_settings.yaml')
)

model_const = load_yaml(
    os.path.join(_base_dir, 'constants/model_const.yaml')
)

def update_settings(dict_, new_dict):
    for k, v in new_dict.items():
        if isinstance(v, collections.abc.Mapping):
            dict_[k] = update_settings(dict_.get(k, {}), v)
        else:
            dict_[k] = v
    return dict_

def update_modifications(tsv:str="",
    keep_only_important_modloss:bool=global_settings['common']['keep_only_important_modloss']
):
    if os.path.isfile(tsv):
        load_mod_df(tsv, keep_only_important_modloss=keep_only_important_modloss)

        from peptdeep.model.featurize import get_all_mod_features
        get_all_mod_features()
    else:
        if keep_only_important_modloss:
            _keep_only_important_modloss()

update_modifications()