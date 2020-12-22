import numpy as np
import pandas as pd


class DataReader:

    def __init__(self, cfg):
        self.config = cfg
        self._dataset = None
        self._num_user = None
        self._num_item = None
        self.dataset

    @property
    def dataset(self):
        if self._dataset is None:
            self._dataset = pd.read_csv(**self.config,
                                        engine='python')
            self._num_item = int(self._dataset[['itemId']].nunique())
            self._num_user = int(self._dataset[['userId']].nunique())

        return self._dataset

    @property
    def path(self):
        return self.config['path']

    @property
    def header(self):
        return self.config.get('header', 'infer')

    @property
    def names(self):
        return self.config.get('names')

    @property
    def sep(self):
        return self.config.get("sep", ",")

    def make_consecutive_ids_in_dataset(self):
        # TODO: create mapping function
        dataset = self.dataset.rename({
                    "userId": "user_id",
                    "itemId": "item_id"
                }, axis=1)

        user_id = dataset[['user_id']].drop_duplicates().reindex()
        num_user = len(user_id)

        user_id['userId'] = np.arange(num_user)
        self._dataset = pd.merge(
            dataset, user_id,
            on=['user_id'], how='left')

        item_id = dataset[['item_id']].drop_duplicates()
        num_item = len(item_id)
        item_id['itemId'] = np.arange(num_item)

        self._dataset = pd.merge(
            self._dataset, item_id,
            on=['item_id'], how='left')

        self.origina_user_id = user_id
        self.origina_item_id = item_id

        self._dataset = self.dataset[
            ['userId', 'itemId', 'rating', 'timestamp']
        ]

        self._dataset.userId = [int(i) for i in self._dataset.userId]
        self._dataset.itemId = [int(i) for i in self._dataset.itemId]

    def binarize(self):
        """binarize into 0 or 1, imlicit feedback"""
        self._dataset['rating'][self._dataset['rating'] > 0] = 1.0
        self._dataset = self._dataset[self._dataset['rating'] > 0]

    @property
    def num_user(self):
        return self._num_user

    @property
    def num_item(self):
        return self._num_item

