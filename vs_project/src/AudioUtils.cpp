/**
* �������ƣ��������ţ�ֹͣ���͵���������С
*/

#include "AudioUtils.h"
#include "LAppDefine.hpp"

using namespace LAppDefine;


#if 0
char* AudioUtils::LoadWavAsBytes(const char* path, int* size) {
	struct stat statbuf;
	stat(path, &statbuf);
	*size = (int)statbuf.st_size;
	char* bytes = new char[*size];
	std::ifstream ifs(path, std::ios::in | std::ios::binary);
	if (ifs.fail()) {
		if (DebugLogEnable)
			printf("[APP][Audio]file open error: %s\n", path);
		return NULL;
	}
	ifs.read(bytes, *size);
	ifs.close();
	if (DebugLogEnable)
		printf("[APP][Audio]Load Bytes: %s\n", path);
	return bytes;
}

void AudioUtils::ReleaseWavBytes(char* bytes, const char* path) {
	delete[] bytes;
	if (path != NULL && DebugLogEnable) printf("[APP][Audio]Delete Bytes: %s\n", path);
}

void AudioUtils::ResizeVolume(char* bytes, int bufSize, double vol) {
	//��ȡpcm���ݳ���
	//pcm���ݳ����ڵ�40��byte����44��byte
	int pcmLength;
	char str[5];
	if (DebugLogEnable) {
		for (int i = 0, offset = 8; i < 4; i++) {
			str[i] = bytes[offset + i];
		}
		str[4] = '\0';
		printf("[APP][Audio]Format: %s\n", str);
		printf("[APP][Audio]Audio Format: %d\n", *(short*)(bytes + 20));
		printf("[APP][Audio]Num Channels: %d\n", *(short*)(bytes + 22));
		printf("[APP][Audio]Sample Rate: %d\n", *(int*)(bytes + 24));
		printf("[APP][Audio]Byte Rate: %d\n", *(int*)(bytes + 28));
		printf("[APP][Audio]Block Align: %d\n", *(short*)(bytes + 32));
		printf("[APP][Audio]Bits Per Sample: %d\n", *(short*)(bytes + 34));
	}

	//BitsPerSample
	int BitsPerSample = *(short*)(bytes + 34);
	//����16λ������
	if (BitsPerSample != 16) {
		if (DebugLogEnable)
			printf("[AudioUtils]Unhandled BitsPerSample: %d\n", BitsPerSample);
		return;
	}
	for (int i = 0, offset = 36; i < 4; i++) {
		str[i] = bytes[offset + i];
	}
	str[4] = '\0';
	if (DebugLogEnable)
		printf("[APP][Audio]SubChunk2ID: %s\n", str);
	short wData; long dwData;
	int offset, type;
	if (strcmp(str, "data") == 0) {
		pcmLength = bufSize;
		offset = 44;
		type = 0;
	}
	else if (strcmp(str, "LIST") == 0) {
		// ��ʽת����������
		// 36~40 LIST
		// 44~52 INFOISFT
		// 56~60 Lavf
		// 60~70 56.10.100\x00 {codec}
		pcmLength = bufSize;
		offset = 74;
		type = 1;
		return;
	}
	else {
		if (DebugLogEnable)
			printf("[APP][Audio]Unknown SubChunk2ID: %s\n", str);
		return;
	}
	//pcm�������±�44��pcmLength-1�±괦֮��
	for (int pcmPtr = offset; pcmPtr < pcmLength; pcmPtr ++) {
		// pcm����������byte��ʾһ��������ݣ�������һ��short����
		// makeword ���߰�λ�͵Ͱ�λbit�ϳ�һ���������
		wData = MAKEWORD(bytes[pcmPtr], bytes[pcmPtr + 1]);
		// ��long int �����ֹ��vol������
		dwData = wData;
		dwData = dwData * vol;
			
		// ����������Χ
		if (dwData < -0x8000) dwData = -0x8000;
		else if (dwData > 0x7FFF) dwData = 0x7FFF;
		// ��ȡdwData�ĵ�16λ�õ�һ���������
		wData = LOWORD(dwData);
		// ��8λ
		bytes[pcmPtr] = LOBYTE(wData);
		// ��8λ
		bytes[pcmPtr + 1] = HIBYTE(wData);
	}
}
#endif

void AudioUtils::StopSound() {
	PlaySound(NULL, NULL, SND_ASYNC| SND_NODEFAULT);
}

bool AudioUtils::StartSound(const char* path, double vol, bool force) {
	bool success;
	long lrVolume = MAKELONG(INT16_MAX * vol, INT16_MAX * vol);
	waveOutSetVolume(NULL, lrVolume);
	if (DebugLogEnable)
		printf("[APP][Audio]Volume Set: %.2lf\n", vol);
	if (force)
		success = PlaySound(path, NULL, SND_ASYNC | SND_NODEFAULT | SND_FILENAME);
	else
		 success = PlaySound(path, NULL, SND_ASYNC | SND_NOSTOP | SND_NODEFAULT | SND_FILENAME);
	return success;
}

bool AudioUtils::IsSoundPlaying() {
	return !PlaySound(NULL, NULL, SND_NODEFAULT | SND_FILENAME | SND_ASYNC | SND_NOSTOP);
}