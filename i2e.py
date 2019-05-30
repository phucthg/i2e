import cv2;
import numpy as np;
import sys;
import matplotlib.pyplot as plt;
import pandas as pd;
import scipy.interpolate;
from scipy import optimize;
from scipy.interpolate import UnivariateSpline;
from scipy.interpolate import LSQUnivariateSpline;
global file, rx, ry;
moves=[(1, -1), (1, 0), (1, 1)];
def CED(gray, low=600, high=800):
	return cv2.Canny(gray, low, high);
def linear_fit(x:float, a:float, b:float):
	return a*x+b;
def square_fit(x:float, a:float, b:float, c:float):
	return c+x*(b+a*x);
def cubic_fit(x:float, a:float, b:float, c:float, d:float):
	return d+x*(c+(x*(b+x*a)));
def quardatic_fit(x:float, a:float, b:float, c:float, d:float, e:float):
	return e+x*(d+x*(c+(x*(b+x*a))));
def output_poly(f, left, right, x, y):
	global file;
	usable=y+"=";
	for i in range(len(f)):
		if(i>0 and f[i]>0):
			usable+='+';
		usable+="{:.10f}".format(f[i]);
		usable+="*"+x+"^{";
		usable+=str(len(f)-i-1);
		usable+="}";
	usable+="+("+str(right)+"-"+x+")^{0.5}";
	usable+="-("+str(right)+"-"+x+")^{0.5}";
	usable+="+("+x+"-"+str(left)+")^{0.5}";
	usable+="-("+x+"-"+str(left)+")^{0.5}";
	file.write(usable);
	file.write("\n");
def ITP(edges, cut_off=100):
	height=edges.shape[0];
	width=edges.shape[1];
	done=np.zeros(edges.shape);
	xp=np.linspace(0, 100, width);
	global rx, ry;
	for j in range(width):
		for i in range(height):
			if(edges[i][j]==0):
				continue;
			if(done[i][j]):
				continue;
			rx=[];
			ry=[];
			y=i;
			x=j;
			rx.append(x);
			ry.append(height-y-1);
			done[y][x]=1;
			while(True):
				moved=False;
				for move in moves:
					xx=x+move[0];
					yy=y+move[1];
					if(xx<0 or xx>=width):
						continue;
					if(yy<0 or yy>=height):
						continue;
					if(done[yy][xx]):
						continue;
					if(edges[yy][xx]==0):
						continue;
					x=xx;
					y=yy;
					moved=True;
					break;
				if(moved==False):
					break;
				rx.append(x);
				ry.append(height-y-1);
				done[y][x]=1;
			ax=np.array(rx);
			ay=np.array(ry);
			if(len(ax)==1):
				continue;
			temp=None;
			if(len(ax)==2):
				temp=optimize.curve_fit(linear_fit, ax, ay);
			elif(len(ax)==3):
				temp=optimize.curve_fit(square_fit, ax, ay);
			elif(len(ax)==4):
				temp=optimize.curve_fit(cubic_fit, ax, ay);
			else:
				temp=optimize.curve_fit(quardatic_fit, ax, ay);
			output_poly(temp[0], ax[0], ax[len(ax)-1], 'x', 'y');
	done=np.zeros(edges.shape);
	for i in range(height):
		for j in range(width):
			if(edges[i][j]==0):
				continue;
			if(done[i][j]):
				continue;
			rx=[];
			ry=[];
			x=i;
			y=j;
			rx.append(height-x-1);
			ry.append(y);
			done[x][y]=1;
			while(True):
				moved=False;
				for move in moves:
					xx=x+move[0];
					yy=y+move[1];
					if(xx<0 or xx>=height):
						continue;
					if(yy<0 or yy>=width):
						continue;
					if(done[xx][yy]):
						continue;
					if(edges[xx][yy]==0):
						continue;
					x=xx;
					y=yy;
					moved=True;
					break;
				if(moved==False):
					break;
				rx.append(height-x-1);
				ry.append(y);
				done[x][y]=1;
			rx.reverse();
			ry.reverse();
			ax=np.array(rx);
			ay=np.array(ry);
			if(len(ax)==1):
				continue;
			temp=None;
			if(len(ax)==2):
				temp=optimize.curve_fit(linear_fit, ax, ay);
			elif(len(ax)==3):
				temp=optimize.curve_fit(square_fit, ax, ay);
			elif(len(ax)==4):
				temp=optimize.curve_fit(cubic_fit, ax, ay);
			else:
				temp=optimize.curve_fit(quardatic_fit, ax, ay);
			output_poly(temp[0], ax[0], ax[len(ax)-1], 'y', 'x');
def main(args):
	global file;
	id=args[0];
	low=None;
	high=None;
	if(len(args)==3):
		low=int(args[1]);
		high=int(args[2]);
	else:
		low=400;
		high=600;
	image=cv2.imread(id, cv2.IMREAD_GRAYSCALE);
	edges=CED(image, low, high);
	cv2.imshow('images', edges);
	file=open("output.txt", "w+");
	ITP(edges);
	file.flush();
	file.close();
	cv2.waitKey(0);
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
