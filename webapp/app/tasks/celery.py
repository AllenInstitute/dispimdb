import os
import subprocess
import sys

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)

from acpreprocessing import downsampling
from acpreprocessing.utils import io, convert
from app.tasks.save_gif_bdvCR import run
from app.tasks import imagej

from app import celery
from app.db import get_db
from . import bp

def stripfile(output_dir, input_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    index = 0

    for p in range(1,18):
        input_file = "/ispim2_data/mus_541177_sec22_0.5xpbs_upper_left_quad/ex1_0000/ex1_0000_MMStack_Pos1_%d.ome.tif"%p
        I = io.get_tiff_image(input_file)
        for j in range(I.shape[0]):
            img = I[j,:,:]
            print(img.shape)
            fname = "/allen/programs/celltypes/workgroups/em-connectomics/analysis_group/forSharmi/axonal/testdata/pos1/{0:05d}.tif".format(index)
            io.save_tiff_image(img, fname)
            print(fname)
            index += 1

@celery.task
def generate_gif():
    savepositions = ['21','22','23','24','25','26','27','28','29','30']
    mntpath = "/ispim1_data/"
    subpath = "PoojaB/20210127/490421_15_GFP_lightsheet_l100_"
    for pos in savepositions:
        savename = 'Pos0' + pos
        subpath = "PoojaB/20210127/490421_15_GFP_lightsheet_l100_" + savename
        savepath = "/home/samk/acworkflow/" + savename
    
        run(os.path.join(mntpath, subpath),savepath,savename)

@celery.task
def generate_gifs_ijm(input):
    imagej.run_imagej(ijm_input=input, script='macro')

@celery.task
def slice_tiff_to_n5():
    script_dir = ""
    input_dir = ""
    output_dir = ""

    #check if files already exist
    stripfile(output_dir, input_dir)

    cmd = ["python", os.path.join(script_dir, "slice-tiff-to-n5.py"),
           "-i", output_dir,
           "-n", output_dir + "_n5",
           "-o", "allstacks",
           "-b", "64,64,32"]

    subprocess.run(cmd)

@celery.task
def n5_scale_pyramid():
    script_dir = ""
    output_dir = ""
    input_file = ""

    stripfile(output_dir, input_file)

    cmd = ["python", os.path.join(script_dir, "n5-scale-pyramid.py"),
           "-n", "",
           "-i", "",
           "-f", "",
           "-o", ""]
    
    subprocess.run(cmd)

@celery.task
def add(x, y):
    return x + y

@celery.task
def mul(x, y):
    return x * y

@celery.task
def xsum(numbers):
    return sum(numbers)