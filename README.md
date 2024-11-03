# PL-LogicalConsistency
This repository is used to test the logical consistency of code generation LLMs.   

We only run GPT-2, CodeGemma-2B, and CodeGen-2B-Mono locally.
To find our applications for Phi-3-Mini-4K-Instruct and CodeLlama-7B, please visit [CodeLC.ipynb](https://colab.research.google.com/drive/1kMmLhe2VuIQl4IgM50cO0yh8fh8y7Fos#scrollTo=mI7tKa5zhPPm) on Google Colab.

The directory of the repository lists as follows:

```
project_root/
├── CodeLC.ipynb                     # Main application file.
├── syn_data                          # Data sampled by the Logic Filter. Original data from CodeSearchNet Python dataset.
│   ├── py_20                         # A quick test dataset with only 20 code examples.
│   │   ├── LI_ori_full.json              # Original sub-dataset for FIM task.
│   │   ├── LI_ori_trct.json              # Original sub-dataset for NOP task.
│   │   ├── LI_ori_full_no_comments.json  # No Comment sub-dataset for FIM task.
│   │   ├── LI_ori_trct_no_comments.json  # No Comment sub-dataset for NOP task.
│   │   ├── LI_pure_full.json             # No Context sub-dataset for FIM task.
│   │   └── LI_pure_trct.json             # No Context sub-dataset for NOP task.
│   │
│   └── py_full                           # The full test dataset.
│      ├── LI_ori_full.json              # Original sub-dataset for FIM task.
│      ├── LI_ori_trct.json              # Original sub-dataset for NOP task.
│      ├── LI_ori_full_no_comments.json  # No Comment sub-dataset for FIM task.
│      ├── LI_ori_trct_no_comments.json  # No Comment sub-dataset for NOP task.
│      ├── LI_pure_full.json             # No Context sub-dataset for FIM task.
│      └── LI_pure_trct.json             # No Context sub-dataset for NOP task.
│
├── result                            # The experimental results.
│   └── alys                          # The experimental results analysis.
│
└── logical_utils                     # Dependency package. For code on Google Colab, please import logical_utils.
