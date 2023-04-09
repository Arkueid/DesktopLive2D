#pragma once
#include <iostream>
#include <fstream>
#include <windows.h>
#include <sys/stat.h>

namespace AudioUtils{
	/** 
	* @brief	��ȡ.wav�ļ�
	* @param	path	wav�ļ�·��
	* @param	size	wav�ļ���С
	* @param	Log		�ص���־����
	*/
	char* LoadWavAsBytes(const char* path, int* size);

	/**
	* @brief	�ͷŴ���wav���ݵ��ڴ�
	* @param	bytes	wav���ݴ������ָ��
	* @param	path	wav�ļ�·��
	* @param	Log		�ص���־����
	*/
	void ReleaseWavBytes(char* bytes, const char* path = NULL);

	/**
	* @brief	����wav��Ƶ����
	* @param	bytes	wav����ָ��
	* @param	bufSize	�����С
	* @param	vol		�������ű���, 0-1֮�両����
	*/
	void ResizeVolume(char* bytes, int bufSize, double vol);

	/**
	* @brief	ֹͣ���ڲ��ŵ���Ƶ
	*/
	void StopSound();

	/**
	* @brief	������Ƶ
	* @param	path	��Ƶ·������wav
	* @param	vol		�������ű���, 0-1֮��ĸ�����
	*/
	bool StartSound(const char* path, double vol, bool force = false);

	/**
	* @brief	�Ƿ��������ڲ���
	*/
	bool IsSoundPlaying();
}