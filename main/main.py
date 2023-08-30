import cv2
import numpy as np

# Завантаження зображення чашки зі зеленою областю та зображення для вставки
object_with_green_area_path = 'image4.png'
photo_path = 'photo.png'

# Завантаження зображень
cup_with_green_area = cv2.imread(object_with_green_area_path)
photo = cv2.imread(photo_path)

# Конвертація до HSV простору кольорів
hsv_cup = cv2.cvtColor(cup_with_green_area, cv2.COLOR_BGR2HSV)

# Зелений діапазон у HSV
lower_green = np.array([35, 50, 50])
upper_green = np.array([85, 255, 255])

# Виділення зелених областей
mask = cv2.inRange(hsv_cup, lower_green, upper_green)

# Знаходження всіх зелених пікселів
green_pixels = np.where(mask > 0)

# Знаходження вписаного прямокутника в зелену область
x, y, w, h = cv2.boundingRect(np.array(list(zip(green_pixels[1], green_pixels[0]))))

# Визначення афінного перетворення
src_pts = np.array([[0, 0], [photo.shape[1] - 1, 0], [0, photo.shape[0] - 1]], dtype=np.float32)
dst_pts = np.array([[x, y], [x + w - 1, y], [x, y + h - 1]], dtype=np.float32)
affine_matrix = cv2.getAffineTransform(src_pts, dst_pts)

# Застосування афінного перетворення до зображення для вставки
warped_photo = cv2.warpAffine(photo, affine_matrix, (cup_with_green_area.shape[1], cup_with_green_area.shape[0]))

# Заміна зелених пікселів на пікселі з вставленого зображення
cup_with_green_area[mask > 0] = warped_photo[mask > 0]

# Збереження результату
result_path = 'cup_with_replaced_green_area.png'
cv2.imwrite(result_path, cup_with_green_area)

print(f"Зображення збережено як {result_path}")
