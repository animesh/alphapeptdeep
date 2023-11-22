#!/bin/sh
#SBATCH --account=nn9036k --job-name=PEPDEEP
#SBATCH --time=48:00:00
##SBATCH --partition=bigmem
##SBATCH --ntasks=16 --cpus-per-task=4
##SBATCH --mem-per-cpu=32G
#SBATCH --ntasks=1 --cpus-per-task=10
#SBATCH --mem-per-cpu=4G
#SBATCH --mail-user=animesh.sharma@ntnu.no
#SBATCH --mail-type=ALL
#SBATCH --output=PEPDEEP
conda activate peptdeep
WORKDIR=${PWD}
$HOME/.conda/envs/peptdeep/bin/peptdeep library settings.yaml
