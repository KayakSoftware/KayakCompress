import folium
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys, getopt
import traceback
#Suggested epsilon value: 0.00001


#We borrow implementation of dist function from lecutre on distance in MASD 2018 at KU.
def pldist(point, start, arrLength):

    if np.all(np.equal(start, arrLength)):
        return np.linalg.norm(point - start)

    return np.divide(
            np.abs(np.linalg.norm(np.cross(arrLength - start, start - point))),
            np.linalg.norm(arrLength - start))

#Shortcomings: Consider convex-hull
#Shortcomings: In an ideal world it should use a timeseries based distance measure, probably not needed due to low fequency in speed change in a kayak.
#Shortcomings: Currently reshaping everytime we build the result to handle edge-cases, and the result even if not needed, dont.
def RamerDouglasPeucker(PointArray, epsilon):
	maxDistance = 0
	index = 0
	arrLength = len(PointArray)

	for idx in range(1, arrLength-1):
		dist = pldist(PointArray[idx], PointArray[0], PointArray[arrLength-1])
		if dist > maxDistance:
			index = idx
			maxDistance = dist

	#We check if the maximum current distance is greater than epsilon, if yes then we recursviely simplify
	if maxDistance > epsilon:
		#The recursive Devide and Conquer calls.
		recResults1 = RamerDouglasPeucker(PointArray[1:index], epsilon)
		recResults2 = RamerDouglasPeucker(PointArray[index:arrLength-1], epsilon)
		#Build our result, reshape for numpy edge-cases.
		ResultList = np.concatenate((np.reshape(recResults1, (-1,2)), np.reshape(recResults2, (-1,2))))
	else:
		if len(PointArray) < 3:
			ResultList = np.copy(PointArray)
		else:
			ResultList = np.concatenate((PointArray[0], PointArray[arrLength-1]))
	#Reshape for a few edge-cases with numpy
	return np.reshape(ResultList, (-1,2))


def main(argv):
	if (len(sys.argv) != 3) and (len(sys.argv) != 4):
		print("Failed compression: Requires one inputfile, an error value and at most one option.\n compress.py <file> <error> <option> -test -log")
		sys.exit(1)
	else:
		try:
			df = pd.read_csv(sys.argv[1])
			df = df[df.columns[1:3]]
			coords = df.to_numpy()
			epsilon = float(sys.argv[2])

			if len(sys.argv) == 4 and sys.argv[3] == '-test':
				#Create  and save baseline map
				m = folium.Map(coords[0], zoom_start=15)
				folium.PolyLine(coords).add_to(m)
				m.save('testMapPreCompress.html')

				#Create map, compress and save.
				m2 = folium.Map(coords[0], zoom_start=15)
				res = RamerDouglasPeucker(coords, epsilon)
				folium.PolyLine(res).add_to(m2)
				m2.save('testMapPostCompress.html')

			elif len(sys.argv) == 4 and sys.argv[3] == '-log':
				res = RamerDouglasPeucker(coords, epsilon)
				print(len(coords))
				print(coords)
				print(len(res))
				print(res)

			elif len(sys.argv) == 3:
				res = RamerDouglasPeucker(coords, epsilon)
				
			else:
				raise RuntimeError("Failed compression: Requires one inputfile, an error value and at most one option.\n compress.py <file> <error> <option> -test -log")

			print("From {} coordinates, to {} coordinates".format(len(res), len(coords)))
			reduction = (len(res)/len(coords)) * 100
			print("Compressed amount of coordinates to {:.2f}% of original size.".format(reduction))
			
			resDf = pd.DataFrame(res, columns=['lattitude,', 'longitude'])
			resDf.to_csv(r'./compressedCoords.csv')


		except FileNotFoundError:
			print("Failed compression: Input file does not exist.")
		except Exception as e:
			traceStack = traceback.format_exc()
			print("Failed compression:\n {} \n {}".format(traceStack, e))
		finally:
			sys.exit(2)

if __name__ == "__main__":
	main(sys.argv)