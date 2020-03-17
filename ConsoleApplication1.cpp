// ConsoleApplication1.cpp : This file contains the 'main' function. Program execution begins and ends there.

#include <iostream>
#include <fstream>
#include <ctime>
#include <opencv2/opencv.hpp>
// #include <opencv2/videoio.hpp>

using namespace std;
using namespace cv;

int main()
{
	ofstream file;
	file.open("Average Frame Values CPP.txt");

	String path;
	cout << "Provide the absolute path of yor video:" << endl;
	cin >> path;
	VideoCapture cap(path);
	Mat frame;

	if (!cap.isOpened()) {
		cout << "Error when trying to read '.mp4' file." << endl;
	} else {
		cout << "Able to read video file. Poceeding..." << endl;
	}

	
	int fps = cap.get(CAP_PROP_FPS);
	int totalFrames = cap.get(CAP_PROP_FRAME_COUNT);
	int framesToRead = totalFrames / fps;
	cout << "Frames per second: " << fps << endl;
	cout << "Total Frames in Video: " << totalFrames << endl;
	cout << "Frames to read from video: " << framesToRead << endl;

	auto time = chrono::system_clock::now();
	std::time_t start_time = std::chrono::system_clock::to_time_t(time);
	cout << "Starting..." << start_time << endl;
	int red;
	int green;
	int blue;
	int pixels;
	int x = 0;
	int frameCounter = 0;
	for (int i = 0; i < framesToRead; i++) {
		cap.read(frame);

		red = 0;
		green = 0;
		blue = 0;
		pixels = 0;

		int cn = frame.channels();
		Scalar_<uint8_t> bgrPixel;
		for (int i = 0; i < frame.rows; i++) {
			for (int j = 0; j < frame.cols; j++) {
				Vec3b bgrPixel = frame.at<Vec3b>(i, j);
				blue += bgrPixel[0];
				green += bgrPixel[1];
				red += bgrPixel[2];
				pixels += 1;

			}

		}
		int avg_red = red / pixels;
		int avg_green = green / pixels;
		int avg_blue = blue / pixels;
		file << "Frame" << x << ":" << avg_red << "," << avg_green << "," << avg_blue << "\n";
		if (frameCounter + fps < totalFrames) {
			frameCounter += fps;
			cap.set(1, frameCounter);
		} else {
			break;
		}
		
		x += 1;
	}

	auto end_time = chrono::system_clock::now();
	time_t done_time = chrono::system_clock::to_time_t(end_time);
	cout << "Complete. " << done_time << endl;
	file.close();
	return 0;
}
