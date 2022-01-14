import os
import subprocess
import time

imagej_config = {
    'imagej_path': '/home/samk/Fiji.app/ImageJ-linux64'
}

test_input = {
    'macro_path': '/home/samk/acworkflow/app/tasks/ijm',
    'macro': 'test.ijm',
    'args': {
        'tiff_path': '/ispim2_data/541177_23_NeuN_NFH_488_16X_05XPBS/ex1',
        'gif_path': '/home/samk/ijm_test/ds_gifs'
    }
}

def run_imagej(ijm_input=test_input, script='macro'):
    arglist = [ijm_input['args']['tiff_path'],
            ijm_input['args']['gif_path']]
    
    if not os.path.exists(ijm_input['args']['gif_path']):
        os.makedirs(ijm_input['args']['gif_path'])
    
    argdelim = "#"
    argstring = argdelim.join(arglist)
    print(argstring)
    imagej_cmd = []

    if script == 'macro':
        imagej_cmd = [imagej_config['imagej_path'],
                    '--headless',
                    '-macro', os.path.join(ijm_input['macro_path'], ijm_input['macro']),
                    argstring]
    
    print(imagej_cmd)
    subprocess.run(imagej_cmd)

if __name__ == '__main__':
    start = time.time()
    run_imagej(ijm_input=test_input, script='macro')
    stop = time.time()