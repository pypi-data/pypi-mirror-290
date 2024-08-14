__all__ = [
    'TrainingDataset',
    'get_loaders'
]
import glob
import torch
# import nibabel as nib
import cornucopia as cc
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision.transforms import Compose, RandomApply


def _transform(x, y, device='cuda'):
    x, y = x.to(device), y.to(device)

    x, y = cc.RandomFlipTransform()(x, y)
    x, y = cc.RandomFlipTransform()(x, y)
    x, y = cc.AffineElasticTransform()(x, y)
    transforms = Compose([
        cc.QuantileTransform(vmin=-1, vmax=1),
        RandomApply([cc.GaussianNoiseTransform()]),
        RandomApply([cc.RandomGammaTransform()]),
        cc.QuantileTransform(vmin=-1, vmax=1),
        RandomApply([cc.ClipTransform(vmin=-1, vmax=1)]),
        RandomApply([cc.ContrastLookupTransform(1)]),
        cc.QuantileTransform(vmin=-1, vmax=1),
        ])
    x = transforms(x)
    return x, y


class TrainingDataset(Dataset):

    def __init__(self, transform=_transform, data_path: str = None):
        default_path = (
            '/autofs/cluster/octdata2/users/epc28/oct_tissuemasking/data/'
            'training_data'
            )
        path = data_path if data_path else default_path
        self.transform = transform
        self.x_paths = sorted(glob.glob(f'{path}/x/*'))
        self.y_paths = sorted(glob.glob(f'{path}/y/*'))

    def __len__(self):
        return len(self.x_paths)

    def __getitem__(self, idx):
        x = torch.load(self.x_paths[idx])
        y = torch.load(self.y_paths[idx])
        if self.transform:
            if x.min() != x.max():
                x, y = self.transform(x, y)
        return x, y


def get_loaders(
        transform=None, subset=-1, batch_size=1, train_split=0.8,
        seed=42, data_path: str = None):
    """
    Loads and splits data into training and validation sets.

    Parameters
    ----------
    transform : callable
        A function/transform that takes in an image and returns a transformed
        version.
    data_path : str
        Path to the data.
    subset : int, optional
        Number of samples to use. If -1, use the entire dataset. Default is -1.
    batch_size : int, optional
        Number of samples per batch to load. Default is 1.
    train_split : float, optional
        Proportion of the dataset to include in the training split. Default is
        0.8.
    seed : int, optional
        Random seed for reproducibility. Default is 42.

    Returns
    -------
    train_loader : DataLoader
        DataLoader for the training set.
    val_loader : DataLoader
        DataLoader for the validation set.
    """
    dataset = TrainingDataset(data_path=data_path)

    if subset > 0:
        dataset = torch.utils.data.Subset(dataset, range(subset))

    train_size = int(train_split * len(dataset))
    val_size = len(dataset) - train_size

    train_set, val_set = random_split(
        dataset, [train_size, val_size],
        generator=torch.Generator().manual_seed(seed)
    )

    train_loader = DataLoader(
        train_set, batch_size=batch_size, shuffle=True
    )

    val_loader = DataLoader(
        val_set, batch_size=1, shuffle=False
    )

    return train_loader, val_loader
