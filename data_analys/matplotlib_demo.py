import matplotlib.pyplot as plt
import numpy as np

def main():
    x = np.linspace(-np.pi,np.pi,256,endpoint=True)
    c,s = np.cos(x),np.sin(x)
    plt.figure()
    plt.plot(x,c)
    plt.plot(x,s)
    plt.show()








if __name__ == '__main__':
    main()