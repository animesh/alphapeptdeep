#wget "https://figshare.com/ndownloader/files/36246219" -O alphaPepDL.zip 
git clone https://github.com/animesh/alphapeptdeep
cd alphapeptdeep/
conda create --name peptdeep python=3.9 -y
conda activate peptdeep
pip install -e ".[development]"
$HOME/.local/bin/peptdeep -h
$HOME/.local/bin/peptdeep  export-settings settings.yaml
mkdir /cluster/projects/nn9036k/peptdeep
$HOME/.conda/envs/peptdeep/bin/peptdeep library settings.yaml

how 