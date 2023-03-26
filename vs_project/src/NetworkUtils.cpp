#define CPPHTTPLIB_OPENSSL_SUPPORT
#include <httplib.h>
#include "NetworkUtils.h"
#include <QtCore/qdir.h>



using namespace std;
using namespace httplib;

void Log(const char* handler, const char* msg)
{
	if (LAppDefine::DebugLogEnable) printf("[APP]%s: %s\n", handler, msg);
}

namespace BgmListUtils {

	string _BgmListJsonPath = "bgmlist.json";  //�����б�·��

	//���ݵ�ǰϵͳʱ���ж��Ƿ�Ӧ�ø���
	bool ShouldUpdate()
	{
		time_t t;
		time(&t);
		struct tm* now = localtime(&t);
		int weeks[7] = { 6, 0, 1, 2, 3, 4, 5};
		_BgmListJsonPath = string("bangumi.").append(to_string(now->tm_year + 1900)).append(to_string(now->tm_yday - weeks[now->tm_wday])).append(".json");
		if (_access(_BgmListJsonPath.c_str(), 0)==-1) return true;
		return false;
	}

	bool UpdateBgmList()
	{
		Client cli("https://api.bgm.tv");
		Json::Reader reader;
		Json::Value json;
		Result rsp = cli.Get("/calendar");
		if (rsp.error() != Error::Success) return false;
		reader.parse(rsp.value().body, json);
		cli.stop();
		ofstream ofs(_BgmListJsonPath);
		ofs << json;
		ofs.close();
		return true;
	}

	void CheckUpdate()
	{
		if (ShouldUpdate())
		{
			try {
				Log("[BgmList]Update", "������ȡ�����б�...");
				bool ret = UpdateBgmList();
				if (ret)
					Log("[BgmList]Update", string("�����б�������: ").append(_BgmListJsonPath).c_str());
				else Log("[BgmList]Update", "�����б����ʧ��!");
			}
			catch (...)
			{
				Log("[BgmList]Exception", "���������ӣ�������ȡ��!");
			}
		}
		else {
			Log("[BgmList]Update", "�����б��������£�������£�");
		}
	}
}

namespace HolidayUtils
{
	string _HolidayJsonPath = "year.json";
	const bool _DebugLogEnable = true;
	bool GetHolidayJson()
	{
		Log("[Holiday]Update", "������ȡ�����б�...");
		Client cli("https://timor.tech");
		Json::Value json;
		Json::Reader reader;
		Result res = cli.Get("/api/holiday/year");
		if (res.error() != Error::Success) return false;
		reader.parse(res.value().body, json);
		cli.stop();
		ofstream ofs(_HolidayJsonPath, ios::binary);
		ofs << json;
		ofs.close();
		return true;
	}

	bool ShouldUpdate()
	{
		time_t t;
		time(&t);
		struct tm* now = localtime(&t);
		_HolidayJsonPath = string("holiday.") + to_string(now->tm_year + 1900).append(".json");
		if (_access(_HolidayJsonPath.c_str(), 0)==-1) return true;
		return false;
	}

	void CheckUpdate()
	{
		if (ShouldUpdate())
		{
			try {
				bool ret = GetHolidayJson();
				if (ret)
					Log("[Holiday]Update", string("�����б�������: ").append(_HolidayJsonPath).c_str());
				else Log("[Holiday]Exception", "�����б����ʧ��!");
			}
			catch (...)
			{
				Log("[Holiday]Exception", "���������ӣ�������ȡ��!");
			}
		}
		else {
			Log("[Holiday]Update", "�����б��������£�������£�");
		}
	}

	const char* WhatsToday()
	{
		ifstream ifs(_HolidayJsonPath);
		if (ifs.fail()) return NULL;
		Json::Value json;
		ifs >> json;
		ifs.close();
		string td = QDateTime::currentDateTime().toString("MM-dd").toStdString();
		Log("[HolidayUtils]Today", td.c_str());
		if (!json["holiday"][td].isNull() && json["holiday"][td]["holiday"].asBool())
		{
			return json["holiday"][td]["name"].asCString();
		}
		return NULL;
	}
}

namespace ChatAPI {

	//������api
	void AskMlyai(const string& msg, string& resText)
	{
		Client cli("https://api.mlyai.com");
		Json::Value data;
		data["content"] = msg;
		data["type"] = 1;
		data["from"] = LAppConfig::_UserName;
		try {
			Result res = cli.Post("/reply", { {"Api-Key", LAppConfig::_ApiKey}, {"Api-Secret", LAppConfig::_ApiSecret} }, data.toStyledString().c_str(), "application/json; charset=UTF-8");
			if (res.error() != Error::Success) {
				resText = QString::fromLocal8Bit("������������Ŷ~").toStdString();
				return;
			}
			Json::Reader reader;
			Json::Value json;
			reader.parse(res.value().body, json);
			QTextCodec* codec = QTextCodec::codecForName("gbk");
			Log("[ChatAI]Response Msg", codec->fromUnicode(json["message"].asCString()));
			if (strcmp(json["code"].asCString(), "00000") == 0)
				resText = QString::fromUtf8(json["data"][0]["content"].asCString()).toStdString();
			else {
				resText = QString::fromUtf8(json["message"].asCString()).toStdString();
			}
		}
		catch (...)
		{
			resText = QString::fromLocal8Bit("������������Ŷ~").toStdString();
		}
	}

	//�Զ�������������ӿ�
	void Chat(const string& text, string& resText, string& soundPath)
	{
		Client cli(LAppConfig::_CustomChatServerHostPort);
		Headers headers = {
			{"User-Agent", "DesktopLive2D/0.3.0(cpp; cpp-httplib; OpenSSL)"},
			{"Accept-Charset", "UTF-8"},
			{"Accept", "audio/wav"}
		};
		Params params = {
			{"Text", text}
		};
		string body;
		//�����ʱ��
		cli.set_connection_timeout(LAppConfig::_CustomChatServerReadTimeOut);
		//��ȴ���Ӧʱ��
		cli.set_read_timeout(LAppConfig::_CustomChatServerReadTimeOut);
		try {
			auto res = cli.Get(
				LAppConfig::_CustomChatServerRoute, params, headers,
				[&body](const char* data, size_t data_length)->bool
				{
					body.append(data, data_length);
					return true;
				}
			);
			if (res.error() != Error::Success)
			{
				Log("[ChatApi]Exception", "����ʧ��!");
				resText = QString::fromLocal8Bit("�޷����ӵ�������!").toStdString();
				soundPath.clear();
				return;
			};
			QString filename = QDateTime::currentDateTime().toString("yyyyMMddhhmmss").append(".wav");
			soundPath = QString::fromUtf8(LAppConfig::_ChatSavePath.c_str()).append("/").append(filename).toLocal8Bit().constData();
			if (!body.empty())
			{
				ofstream ofs(soundPath.c_str(), ios::binary);
				ofs << body;
				ofs.close();
			}
			else {
				soundPath.clear();
			}
			resText = res.value().get_header_value("Text");
		}
		catch (...)
		{
			resText = QString::fromLocal8Bit("�������Ӵ�����������״��!").toStdString();
			soundPath.clear();
		}
		
	}

	const char* VoiceChat(const char* filePath, string& text, string& soundPath) {
		ifstream ifs(filePath, ios::in | ios::binary);
		if (ifs.fail()) {
#ifdef CONSOLE_FLAG
			printf("[VoiceInput]File opening error: %s\n", filePath);
#endif // CONSOLE_FLAG
			return QString::fromLocal8Bit("����ɶҲû˵��").toLocal8Bit().constData();
		}

		struct stat statbuff;
		int size = 0;
		if (stat(filePath, &statbuff) == 0) {
			size = statbuff.st_size;
		}

		char* bytes = new char[size];
		ifs.read(bytes, size);
		ifs.close();

		httplib::Headers headers = {
			{"User-Agent", "DesktopLive2D/0.3.0(cpp; cpp-httplib; OpenSSL)"},
			{"Accept", "text/plain"}
		};

		httplib::Client client(LAppConfig::_CustomChatServerHostPort);
		auto rsp = client.Post(LAppConfig::_CustomVoiceChatRoute, headers, bytes, "audio/pcm;rate=16000");
		if (rsp.error() != Error::Success) {
#ifdef CONSOLE_FLAG
			printf("[VoiceInputUtils]Resopnse receiving error\n");
#endif // CONSOLE_FLAG
			return QString::fromLocal8Bit("û���յ��ظ�~").toUtf8().constData();
		}
		Json::Value res;
		Json::Reader reader;
		reader.parse(rsp.value().body, res);
		if (res["Text"].isNull()) {
			return QString::fromLocal8Bit("ʲôҲû����~").toUtf8().constData();
		}
		return res["Text"].asCString();
	}

}


/**
* @brief VoiceInputUtils ��������
*/
namespace {
	//token
	std::string _token;
	VoiceInputUtils::Audio* _instance = nullptr;
	//�������̣߳�qt�ź���Ҫeventloop���ܷ���
	QEventLoop* lp = nullptr;
}

VoiceInputUtils::Audio* VoiceInputUtils::Audio::CreateInstance() {
	_instance = new Audio;
	return _instance;
}

VoiceInputUtils::Audio* VoiceInputUtils::Audio::GetInstance() {
	return _instance;
}

void VoiceInputUtils::Audio::ReleaseInstance() {
	if (_instance != nullptr) {
		delete _instance;
	}
	_instance = nullptr;
}

VoiceInputUtils::Audio::Audio()
{
	a_file = nullptr;
	a_input = nullptr;
	stopped = false;
	recording = false;
}

VoiceInputUtils::Audio::~Audio()
{
}

/**
* @brief ¼��
* @param dir �����ļ���
* @param deviceIndex ¼���豸���
*/
void VoiceInputUtils::Audio::StartRecord(const char* dir, int deviceIndex) {
	if (stopped) return;
	QAudioDeviceInfo device = QAudioDeviceInfo::defaultInputDevice();
#ifdef CONSOLE_FLAG
	printf("[VoiceInput]Audio input device name: %s\n", device.deviceName().toLocal8Bit().constData());
#endif // CONSOLE_FLAG
	if (device.isNull()) {
#ifdef CONSOLE_FLAG
		printf("[VoiceInput]No audio input device was found\n");
#endif
		return;
	}

	//������Ƶ��ʽ
	QAudioFormat a_format;
	//
	a_format.setByteOrder(QAudioFormat::LittleEndian);
	//������
	a_format.setSampleRate(16000);
	//������
	a_format.setChannelCount(1);
	//����λ��
	a_format.setSampleSize(16);
	//���ñ���
	a_format.setCodec("audio/pcm");

#ifdef CONSOLE_FLAG
	printf("[VoiceInput]Default audio format (%d, %d, %d, %s)\n",
		a_format.sampleRate(),
		a_format.channelCount(),
		a_format.sampleSize(),
		a_format.codec().toStdString().c_str()
	);
#endif // CONSOLE_FLAG

	if (!device.isFormatSupported(a_format)) {
		a_format = device.nearestFormat(a_format);
#ifdef CONSOLE_FLAG
		printf("[VoiceInput]Audio format switch to (%d, %d, %d, %s)\n",
			a_format.sampleRate(),
			a_format.channelCount(),
			a_format.sampleSize(),
			a_format.codec().toStdString().c_str()
		);
#endif // _DEBUG
	}

	QString path = QString("%1/%2").arg(dir).arg("voice-input-temp.pcm");

	QDir cacheDir(LAppConfig::_VoiceCacheDir.c_str());
	if (!cacheDir.exists())
	{
		cacheDir.mkpath(".");
	}

	a_file = new QFile;
	a_file->setFileName(path);
	a_file->open(QIODevice::WriteOnly | QIODevice::Truncate);

#ifdef CONSOLE_FLAG
	printf("[VoiceInput]Voice input save path: %s\n", path.toLocal8Bit().constData());
#endif // CONSOLE_FLAG

	a_input = new QAudioInput(a_format, NULL);
	if (a_input != NULL && a_file != NULL)
	{
		mutex mut;
		mut.lock();
		a_input->start(a_file);
		mut.unlock();
		recording = true;
	}	
	else {
		printf("[VoiceInputUtils]Too much recording in a short time\n");
	}
#ifdef CONSOLE_FLAG
	printf("[VoiceInput]Satrt recording...\n");
#endif // CONSOLE_FLAG
	if (stopped) StopRecord();
}


void VoiceInputUtils::Audio::StopRecord() {
	stopped = true;
#ifdef CONSOLE_FLAG
	printf("[VoiceInput]Stop recording.\n");
#endif // CONSOLE_FLAG
	if (recording = false) return;
	if (a_input != nullptr) {
		if (a_input->state() != QAudio::ActiveState)
		a_input->stop();
		a_input->deleteLater();
	}

	if (a_file != nullptr)
	{
		a_file->close();
		a_file->deleteLater();
	}

	a_input = NULL;
	a_file = NULL;
}

void VoiceInputUtils::StartRecording(){
	if (Audio::GetInstance() != nullptr) {
		return;
	}
	if (lp != nullptr) {
		return;
	}
	lp = new QEventLoop;
	Audio::CreateInstance();
	Audio::GetInstance()->StartRecord(LAppConfig::_VoiceCacheDir.c_str());
	if (lp != nullptr)
	lp->exec();
}

void VoiceInputUtils::StopRecording() {
	if (!Audio::GetInstance()) return;
	if (lp != nullptr) {
		if (lp->isRunning())
		lp->exit();
		lp->deleteLater();
		lp = nullptr;
	}

	Audio::GetInstance()->StopRecord();

	Audio::ReleaseInstance();

}



/**
* @brief ����¼���ļ�������ʶ�������
*/
const char* VoiceInputUtils::DetectSpeech(const char* filePath) {
#ifdef CONSOLE_FLAG
	time_t start = time(0);
#endif // CONSOLE_FLAG

	httplib::Client client("http://vop.baidu.com");
	QFile file;
	file.setFileName(filePath);
	file.open(QIODevice::ReadOnly);
	QByteArray bytes = file.readAll();
	file.close();
	if (bytes.isEmpty()) {
#ifdef CONSOLE_FLAG
		printf("[VoiceInput]Empty record\n");
#endif // CONSOLE_FLAG
		return "";
	}
	std::string scope = std::string("/server_api");
	Json::Value json;
	json["format"] = "pcm";
	json["rate"] = 16000;
	json["channel"] = 1;
	json["cuid"] = "admin-arkueid-0d000721";
	json["token"] = _token;
	json["dev_pid"] = 1537;
	json["len"] = bytes.length();
	json["speech"] = bytes.toBase64().toStdString();
	auto rsp = client.Post(scope, json.toStyledString(), "application/json");
	if (rsp.error() != httplib::Error::Success) {
#ifdef CONSOLE_FLAG
		printf("[VoiceInput]Response receiving error\n");
#endif // CONSOLE_FLAG
		return QString::fromLocal8Bit("�޷�����ٶ�����ʶ�����").toUtf8().constData();
	}
	Json::Value res;
	Json::Reader reader;
	reader.parse(rsp.value().body, res);
	if (res["result"][0].isNull()) {
#ifdef CONSOLE_FLAG
		printf("[VoiceInput]Speech recognizing Fail\n");
		printf("[VoiceInput]Response: %s", rsp.value().body.c_str());
#endif // CONSOLE_FLAG

		return QString::fromLocal8Bit("����ʶ��ʧ��").toUtf8().constData();
	}
#ifdef CONSOLE_FLAG
	printf("[VoiceInput]Speech recognition (%llds): %s\n", time(0) - start, QString::fromUtf8(res["result"][0].asCString()).toLocal8Bit().constData());
#endif // CONSOLE_FLAG
	return res["result"][0].asCString();
}

/**
* @brief �������������ȡtoken
*/
void VoiceInputUtils::GetToken() {
	httplib::Client client("https://aip.baidubce.com");
	string scope = "/oauth/2.0/token";
	httplib::Headers headers = {
		{"User-Agent", "DesktopLive2D/0.3.0(cpp; cpp-httplib; OpenSSL)"}
	};
	httplib::Params params = {
		{"grant_type", "client_credentials"},
		{"client_id", LAppConfig::_BaiduSpeechClientId},
		{"client_secret", LAppConfig::_BaiduSpeechClientSecret}
	};
	auto rsp = client.Post(scope, headers, params);
	if (rsp.error() != httplib::Error::Success) {
#ifdef CONSOLE_FLAG
		printf("[VoiceInputUtils]Resopnse receiving error\n");
#endif // CONSOLE_FLAG
		return;
	}

	Json::Value token;
	Json::Reader reader;

	reader.parse(rsp.value().body, token);

	token["expires_in"].isNull() ? NULL : token["expires_at"] = time(0) + token["expires_in"].asInt64();

	std::ofstream ofs("baidu.speech.token.json");
	if (ofs.fail()) {
#ifdef CONSOLE_FLAG
		printf("[VloiceInput]Token saving error:\n%s\n", token.toStyledString().c_str());
#endif // CONSOLE_FLAG
		ofs.close();
		return;
	}
	ofs << token;
	ofs.close();

#ifdef CONSOLE_FLAG
	printf("[VoiceInput]Speech token update: baidu.speech.token.json\n");
#endif // CONSOLE_FLAG

	if (token["access_token"].isNull())
		return;
	else
		_token = token["access_token"].asCString();
}


/**
* @brief ����Ƿ���Ҫ����token
*/
bool VoiceInputUtils::ShouldUpdateToken() {
	std::ifstream ifs("baidu.speech.token.json");
	if (ifs.fail()) {
		ifs.close();
		return true;
	}
	Json::Value token;
	ifs >> token;
	ifs.close();
	if (token["expires_at"].isNull()) return true;
	else if (token["access_token"].isNull()) return true;
	else if (token["expires_at"].asInt64() < time(0)) return true;
	return false;
}

/**
* @brief ��Ȿ��token�Ƿ���ڣ����ھ͸���
*/
void VoiceInputUtils::CheckUpdate() {
	if (ShouldUpdateToken())
		GetToken();
	else {
		GetLocalToken();
#ifdef CONSOLE_FLAG
		printf("[VoiceInput]Speech token found in local file\n");
#endif // CONSOLE_FLAG

	}
}


/**
* @brief ��ȡ���ش���İٶ�����ʶ��token
*/
void VoiceInputUtils::GetLocalToken() {
	std::ifstream ifs("baidu.speech.token.json");
	if (ifs.fail()) return GetToken();
	Json::Value token;
	ifs >> token;
	ifs.close();
	_token = token["access_token"].asCString();
}

