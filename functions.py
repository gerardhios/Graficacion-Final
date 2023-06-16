import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# from mpl_toolkits.mplot3d import Axes3D
import os
from pathlib import Path
import numpy as np
from chainCodes import contour, show_img
# import ezdxf

def clean_console():
  os.system('cls' if os.name == 'nt' else 'clear')

def open_img(imgData:list):
    if imgData[1].split('.')[1] == 'obj':
        open_3d_img(imgData)
        return
    img = mpimg.imread(imgData[1])
    plt.imshow(img, cmap='gray')
    plt.title(imgData[0])
    plt.axis('off')
    plt.show()

def get_binary_data(data):
    binary_data = []
    # Get the number of voxels and quit the \n
    voxels_data = data[1].split('\n')[0].split(' ')[1:]
    x, y, z = int(voxels_data[0]), int(voxels_data[1]), int(voxels_data[2])
    # Delete the first 4 lines
    data = data[5:]
    # Delete the \n from the data
    data = [d.split('\n')[0] for d in data]

    # Split the data in lists of x elements
    for i in range(0, len(data), x):
        binary_data.append(data[i:i+x])

    # Convert the binary data to a numpy array
    new_binary_data = np.ones((x, y, z), dtype=np.int8)
    for i, d in enumerate(binary_data):
        for j, b in enumerate(d):
            arr = np.array([int(c) for c in b])
            new_binary_data[i][j] = arr

    return new_binary_data


def binary_to_scr(binary_data, name:str):
    scr_file = Path(f'{name}.scr')
    # If the file already exists, delete it
    if os.path.isfile(scr_file):
        os.remove(scr_file)

    # Create the scr file
    with open(scr_file, 'w') as f:
        coords = np.transpose(np.nonzero(binary_data))
        count = 0
        for z, y, x in coords:
            print(f'z: {z}, y: {y}, x: {x}')
            print(f'{count}/{coords.size}')
            # _box c x, y, z c 1
            f.write(f"_box\nc\n{x+.5},{y+.5},{z+.5}\nc\n1\n")
            # Print the progress with the porcentage of the progress
            count += 1
            clean_console()
        f.write("\n")

                        
    # Execute AutoCAD with the scr file as argument
    os.system(f'acad.exe {scr_file}')

def open_3d_img(imgData:list, ret:bool = False):
    file = Path(imgData[1])
    # Get the full path of the file (excluding the file itself)
    filedirectory = str(file.parent.absolute())
    try:
        # Move to the directory where the file is located
        os.chdir(filedirectory)
    except Exception as e:
        print(e)
    # Check if there is a file with the same name but with .binvox extension
    if not os.path.isfile(f'{file.name.split(".")[0]}.binvox'):
        # Execute binvox.exe with the file as argument
        os.system(f'binvox.exe -d 100 {file.name}')
    if not ret:
        # Execute viewvox.exe with the file as argument
        os.system(f'viewvox.exe {file.name.split(".")[0]}.binvox')

    # Execute convertidor.exe with the file as argument
    os.system(f'convertidor.exe {file.name.split(".")[0]}.binvox')

    binary_file = Path(f'voxels.txt')

    data = []

    # Get the data from the file
    with open(binary_file, 'r') as f:
        data = f.readlines()

    # Delete the binary file
    os.remove(binary_file)
    
    # Get the binary data
    binary_data = get_binary_data(data)

    # Return to the directory where the program is located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if ret:
        return binary_data

    # # Save the binary data to a scr file
    # binary_to_scr(binary_data, file.name.split(".")[0])

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.voxels(binary_data, edgecolor='k')
    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z')
    # plt.show()
    # # Create a dfx file
    # doc = ezdxf.new()
    # msp = doc.modelspace()
    # # Add the voxels to the dfx file
    # for i, x in enumerate(binary_data):
    #     for j, y in enumerate(x):
    #         for k, z in enumerate(y):
    #             if z == 1:
    #                 msp.add_point((i, j, k))
    # # Save the dfx file
    # doc.saveas(f'{file.name.split(".")[0]}.dxf')