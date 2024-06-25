import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Path to the image file
image_path = 'D:/VISUALPROJECT/NETPROJECT/imagesas.jpg'

# Read the image
img = mpimg.imread(image_path, format='jpg')

# Plot the image
plt.imshow(img)
plt.axis('off')  # Remove axis labels
plt.show()

