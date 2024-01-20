# Ward Analytics Labels Upload Utility

This utility is used to upload labels to the Ward Analytics Database.

It is for internal use only.

## Installation

```bash
pip install ward-labels-upload
```

## Usage

### Label Upload

```python
from ward_labels_upload import Label, LabelUploader

uploader = LabelUploader(api_key="your_api_key")

# Note that all addresses are normalized to lowercase. This is necessary for blockchains suck as Ethereum.
labels = [
    Label(address="0x12ef3", label="label1", description="description1"),
    Label(address="0x45af6", label="label2", description="description2"),
    Label(address="0x78cs9", label="label3", description="description3"),
]

uploader.upload_labels(labels=labels)
```
The `LabelUploader` class also takes an optional `base_url` parameter. This is the base URL of the Ward Analytics API. It defaults to `https://api.wardanalytics.net`, which is the production API.

### Label Deletion

```python
from ward_labels_upload import Label, LabelUploader

uploader = LabelUploader(api_key="your_api_key")

# Note that all addresses are normalized to lowercase. This is necessary for blockchains suck as Ethereum.
labels = [
    Label(address="0x12ef3", label="label1"),
    Label(address="0x45af6", label="label2"),
    Label(address="0x78cs9", label="label3"),
]

uploader.delete_labels(labels=labels)
```
In the case of deletion, the description field is unnecessary. This happens because a label is uniquely identified by the combination of its address and label.