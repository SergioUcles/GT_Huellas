import cv2
import numpy as np
import os



def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images


# function to display the coordinates of the points clicked on the image
def click_event(event, x, y, flags, params):
    # Clicks botón izquierdo: TERMINACIÓN
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        cv2.circle(imagen, (x, y), 4, (255, 0, 0), -1)
        print('terminación: ', x, ' ', y)

        terminacion_x.append(x)
        terminacion_y.append(y)
        # bifurcacion_x.append(0)
        # bifurcacion_y.append(0)
        cv2.imshow('image', imagen)

        # Cliks botón derecho: BIFURCACIÓN
    if event == cv2.EVENT_RBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        cv2.circle(imagen, (x, y), 4, (0, 0, 255), -1)
        print('bifurcación: ', x, ' ', y)

        bifurcacion_x.append(x)
        bifurcacion_y.append(y)
        # terminacion_x.append(0)
        # terminacion_y.append(0)
        cv2.imshow('image', imagen)


if __name__ == "__main__":

    folder = "huellas"
    imagenes = load_images_from_folder(folder)
    n_imagen = 0

    dirName = 'GT-huellas'
    try:
        # Create target Directory
        os.mkdir(dirName)
        print("Directory ", dirName, " Created ")
    except FileExistsError:
        print("Directory ", dirName, " already exists")

    for imagen in imagenes:
        n_imagen += 1
        terminacion_x = [];
        terminacion_y = []
        bifurcacion_x = [];
        bifurcacion_y = []

        print("Huella 101_", n_imagen)

        # displaying the image
        cv2.imshow('image', imagen)

        # setting mouse hadler for the image and calling the click_event() function
        cv2.setMouseCallback('image', click_event)

        # wait for a key to be pressed to exit
        cv2.waitKey(0)

        # close the window
        cv2.destroyAllWindows()

        while len(terminacion_x) < len(bifurcacion_x):
            for n in range(len(terminacion_x), len(bifurcacion_x)):
                terminacion_x.append(0)
                terminacion_y.append(0)

        while len(terminacion_x) > len(bifurcacion_x):
            for n in range(len(bifurcacion_x), len(terminacion_x)):
                bifurcacion_x.append(0)
                bifurcacion_y.append(0)

        # creo una matriz con los datos
        data = np.array([terminacion_x, terminacion_y, bifurcacion_x, bifurcacion_y])
        data = data.T  # here you transpose your data, so to have it in two columns

        # nombre de los archivos de salida
        datafile_path = "GT-huellas/gt_101_%s.txt" % n_imagen

        with open(datafile_path, 'w+') as datafile_id:
            # here you open the ascii file

            np.savetxt(datafile_id, data, fmt=['%d', '%d', '%d', '%d'])
            # here the ascii file is written.
