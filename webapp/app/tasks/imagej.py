import os
import subprocess
import time

imagej_config = {
    'imagej_path': '/home/samk/Fiji.app/ImageJ-linux64'
}

test_input = {
    'macro_path': '/home/samk/acworkflow/app/tasks/ijm_macros',
    'macro': 'test.ijm',
    'args': {
        'tiff_path': '/mnt/c/Users/samrk/work_files/cortex_strip_1_ds/cortex_strip_NDTiffStack.tif',
        'gif_path': '/mnt/c/Users/samrk/work_files/cortex_strip_1_gifs/cortex_strip_NDTiffStack_1.gif'
    }
}

test_batch_input = {
    'macro_path': '/home/samk/acworkflow/app/tasks/ijm_macros',
    'macro': 'test_batch.ijm',
    'args': {
        'tiff_path': '/mnt/c/Users/samrk/work_files/cortex_strip_1_ds',
        'gif_path': '/mnt/c/Users/samrk/work_files/cortex_strip_1_gifs'
    }
}

def run_imagej(ijm_input=test_input, script='macro'):
    arglist = [ijm_input['args']['tiff_path'],
            ijm_input['args']['gif_path']]
    
    '''
    if not os.path.exists(ijm_input['args']['gif_path']):
        os.makedirs(ijm_input['args']['gif_path'])
    '''
    
    argdelim = "#"
    argstring = argdelim.join(arglist)
    print(argstring)
    imagej_cmd = []

    if script == 'macro':
        imagej_cmd = [imagej_config['imagej_path'],
                    '--headless',
                    '-macro', os.path.join(ijm_input['macro_path'], ijm_input['macro']),
                    argstring]
    
    subprocess.run(imagej_cmd)

if __name__ == '__main__':
    start = time.time()
    run_imagej(ijm_input=test_batch_input, script='macro')
    stop = time.time()