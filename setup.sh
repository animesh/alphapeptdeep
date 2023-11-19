#wget "https://figshare.com/ndownloader/files/36246219" -O alphaPepDL.zip 
git clone https://github.com/animesh/alphapeptdeep
cd alphapeptdeep/
pip install peptdeep --user
$HOME/.local/bin/peptdeep -h
$HOME/.local/bin/peptdeep  export-settings settings.yaml
ln -s /home/ash022/data/NORSTORE_OSL_DISK/NS9036K/peptdeep $HOME/.
/home/ash022/.local/bin/peptdeep library settings.yaml 