from huggingface_hub import snapshot_download
import os

def get_models(dir):
    repository = "ppisljar/slovene_accentuator"
    target_dir = os.path.join(dir, "cnn")

    if not os.path.exists(target_dir):
        local_dir = snapshot_download(repo_id=repository, local_dir=dir)

        print(f"Repository downloaded to: {local_dir}")
    else:
        print(f"Models already downloaded")
