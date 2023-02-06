#include "controlwidget.h"
#include "LApp.h"
#include <fstream>
#include <vector>
#include <io.h>
#include <QtWidgets/qtabbar.h>
#include <QtCore/qregexp.h>
#include <QtGui/qpainter.h>
#include <QtGui/qvalidator.h>
#include <QtWidgets/qfiledialog.h>
#include <QtWidgets/qlayout.h>
#include <QtWidgets/qtreewidget.h>
#include <QtWidgets/qheaderview.h>
#include <QtWidgets/qmessagebox.h>
#include "LAppLive2DManager.hpp"

using namespace LAppConfig;

class Tip : public QWidget
{
public:
	Tip();
	void Pop(QWidget* p, const char* text);
	static Tip* GetInstance();
protected:
	void paintEvent(QPaintEvent* e);
	const char* text = NULL;
	QPropertyAnimation* anime;
};

namespace {
	Tip* _tip = NULL;
}

Tip::Tip()
{
	resize(100, 40);
	setAttribute(Qt::WA_TransparentForMouseEvents);
	setWindowFlags(Qt::ToolTip | Qt::FramelessWindowHint|Qt::WindowStaysOnTopHint);
	anime = new QPropertyAnimation(this, "windowOpacity");
	anime->setStartValue(1);
	anime->setEndValue(0);
	anime->setDuration(2000);
}
void Tip::paintEvent(QPaintEvent* e)
{
	resize(strlen(text) * 7 + 30, 40);
	QPainter painter(this);
	painter.fillRect(0, 0, width(), 40, QColor(0, 0, 0, 180));
	painter.setPen(Qt::white);
	painter.drawText(15, 25, QString::fromLocal8Bit(text).toStdString().c_str());
}
void Tip::Pop(QWidget* p, const char* text)
{
	close();
	this->text = text;
	anime->stop();
	move(p->x() + p->width() / 2 - width()/2, p->y() + 20);
	show();
	anime->start();
}
Tip* Tip::GetInstance()
{
	if (_tip == NULL) _tip = new Tip();
	return _tip;
}


void getDirNames(string path, vector<string>& files)
{
	//�ļ����
#ifdef WIN64_FLAG
	__int64   hFile = 0;
#else
	long	hFile = 0;
#endif // WIN64_FLAG

	//�ļ���Ϣ
#ifdef WIN64_FLAG
	struct __finddata64_t fileinfo;
#else
	struct _finddata_t fileinfo;
#endif // WIN64_FLAG

	string p;
	if (
#ifdef WIN64_FLAG
	(hFile = _findfirst64(p.assign(path).append("\\*").c_str(), &fileinfo)) != -1L
#else
	(hFile = _findfirst(p.assign(path).append("\\*").c_str(), &fileinfo)) != -1
#endif // WIN64_FLAG
		)
	{
		do
		{
			if ((fileinfo.attrib & _A_SUBDIR))
			{
				string x = fileinfo.name;
				if (strcmp(x.c_str(), ".") != 0 && strcmp(x.c_str(), "..") != 0)
				{
					files.push_back(string(fileinfo.name));
				}
			}
		} while (
#ifdef WIN64_FLAG
			_findnext64(hFile, &fileinfo) == 0
#else
			_findnext(hFile, &fileinfo) == 0
#endif // WIN64_FLAG

			);
		_findclose(hFile);
	}
}

void getFileNames(string path, vector<string>& files)
{
	//�ļ����
#ifdef WIN64_FLAG
	__int64   hFile = 0;
	struct __finddata64_t fileinfo;
#else
	long   hFile = 0;
	struct _finddata_t fileinfo;
#endif // WIN64_FLAG

	//�ļ���Ϣ
	string p;
	if (
#ifdef WIN64_FLAG
	(hFile = _findfirst64(p.assign(path).append("\\*").c_str(), &fileinfo)) != -1L
#else
	(hFile = _findfirst(p.assign(path).append("\\*").c_str(), &fileinfo)) != -1
#endif // WIN64_FLAG
		)
	{
		do
		{
			if (!(fileinfo.attrib & _A_SUBDIR))
			{
				files.push_back(string(fileinfo.name));
			}
		} while (
#ifdef WIN64_FLAG
			_findnext64(hFile, &fileinfo) == 0
#else
			_findnext(hFile, &fileinfo) == 0
#endif // WIN64_FLAG
			);
		_findclose(hFile);
	}
}


AppSettings::AppSettings(QWidget* p)
{
	_parent = p;
	lbl_appName = new QLabel(QString::fromLocal8Bit("Ӧ������"));
	lbl_username = new QLabel(QString::fromLocal8Bit("�û�����"));
	lbl_iconPath = new QLabel(QString::fromLocal8Bit("����ͼ��"));
	lbl_FPS = new QLabel("FPS");
	lbl_appKey = new QLabel(QString::fromLocal8Bit("Api-Key"));
	lbl_appSecret = new QLabel(QString::fromLocal8Bit("Api-Secret"));
	lbl_windowWidth = new QLabel(QString::fromLocal8Bit("���ڿ��"));
	lbl_windowHeight = new QLabel(QString::fromLocal8Bit("���ڸ߶�"));
	lbl_modelDir = new QLabel(QString::fromLocal8Bit("��Դ�ļ���"));
	appName = new QLineEdit();
	username = new QLineEdit();
	iconPath = new QLineEdit();
	appKey = new QLineEdit();
	appSecret = new QLineEdit();
	fps = new QLineEdit();
	windowWidth = new QLineEdit();
	windowHeight = new QLineEdit();
	modelDir = new QLineEdit();
	appName->setFixedHeight(30);
	username->setFixedHeight(30);
	iconPath->setFixedHeight(30);
	appKey->setFixedHeight(30);
	appSecret->setFixedHeight(30);
	fps->setFixedHeight(30);
	windowWidth->setFixedHeight(30);
	windowHeight->setFixedHeight(30);
	modelDir->setFixedHeight(30);


	const QValidator* v = new QRegExpValidator(QRegExp("[0-9]{1,2}"));
	fps->setValidator(v);
	const QValidator* v2 = new QRegExpValidator(QRegExp("[0-9]{1,4}"));
	windowWidth->setValidator(v2);
	windowHeight->setValidator(v2);

	openFile = new QPushButton(QString::fromLocal8Bit("���ļ�"));
	chooseDir = new QPushButton(QString::fromLocal8Bit("ѡ���ļ���"));
	apply = new QPushButton(QString::fromLocal8Bit("Ӧ��"));
	cancel = new QPushButton(QString::fromLocal8Bit("����"));

	grid = new QGridLayout();
	grid->addWidget(lbl_appName, 0, 0, 0);
	grid->addWidget(appName, 0, 1, 1, 4, 0);
	grid->addWidget(lbl_username, 0, 5, 0);
	grid->addWidget(username, 0, 6, 1, 4, 0);
	grid->addWidget(lbl_iconPath, 2, 0, 0);
	grid->addWidget(iconPath, 2, 1, 1, 8, 0);
	grid->addWidget(openFile, 2, 9, 0);
	grid->addWidget(lbl_modelDir, 3, 0, 1, 1, 0);
	grid->addWidget(modelDir, 3, 1, 1, 8, 0);
	grid->addWidget(chooseDir, 3, 9, 1, 1, 0);
	grid->addWidget(lbl_windowWidth, 4, 0, 1, 1, 0);
	grid->addWidget(windowWidth, 4, 1, 1, 1, 0);
	grid->addWidget(lbl_windowHeight, 4, 2, 1, 1, 0);
	grid->addWidget(windowHeight, 4, 3, 1, 1, 0);
	grid->addWidget(lbl_FPS, 4, 4, 0);
	grid->addWidget(fps, 4, 5, 1, 1, 0);
	grid->addWidget(lbl_appKey, 5, 0, 0);
	grid->addWidget(appKey, 5, 1, 1, 4, 0);
	grid->addWidget(lbl_appSecret, 6, 0, 0);
	grid->addWidget(appSecret, 6, 1, 1, 4, 0);
	grid->addWidget(apply, 7, 6, 1, 2, 0);
	grid->addWidget(cancel, 7, 8, 1, 2, 0);
	setLayout(grid);
	
	connect(openFile, SIGNAL(clicked()), SLOT(OpenFile()));
	connect(chooseDir, SIGNAL(clicked()), SLOT(OpenSourceDir()));

	connect(apply, SIGNAL(clicked()), SLOT(Apply()));
	connect(cancel, SIGNAL(clicked()), SLOT(Cancel()));
}

void AppSettings::OpenFile()
{
	QString path = QFileDialog::getOpenFileName(this, QString::fromLocal8Bit("ѡ��ͼ��·��"), iconPath->text(), "Image File(*.jpg *.png);;");
	if (!path.isEmpty())
	iconPath->setText(path);
}

void AppSettings::OpenSourceDir()
{
	QString path = QFileDialog::getExistingDirectory(this, QString::fromLocal8Bit("ѡ����Դ�ļ���"), modelDir->text());
	if (!path.isEmpty())
		modelDir->setText(path);
}

void AppSettings::Apply()
{
	_AppName = appName->text().toStdString();
	_UserName = username->text().toStdString();
	_IconPath = iconPath->text().toStdString();
	_ApiKey = appKey->text().toStdString();
	_ApiSecret = appSecret->text().toStdString();
	_FPS = fps->text().toInt() == 0? _FPS : fps->text().toInt();
	_WindowWidth = windowWidth->text().toInt() == 0 ? _WindowWidth : windowWidth->text().toInt();
	_WindowHeight = windowHeight->text().toInt() == 0 ? _WindowHeight : windowHeight->text().toInt();
	_ModelDir = modelDir->text().isEmpty() ? _ModelDir : modelDir->text().toStdString();
	LApp::GetInstance()->GetWindow()->LoadConfig();
	_parent->setWindowTitle(QString::fromStdString(_AppName));
	LoadConfig();
	ControlWidget* p = static_cast<ControlWidget*>(_parent);
	try {
		if (p) {
			p->_modelSettings->LoadConfig();
			Log("[AppSettings]_ModelDir changed: %s", _ModelDir.c_str());
		}
		else Log("[AppSettings]: cast failed", NULL);
		LApp::GetInstance()->SaveConfig();
		Tip::GetInstance()->Pop(_parent, "����ɹ�!");
	}
	catch (exception e)
	{
		Tip::GetInstance()->Pop(_parent, "��Դ·������!");
		LApp::GetInstance()->LoadConfig();
		LoadConfig();
		p->_modelSettings->LoadConfig();
	}
}
void AppSettings::Cancel()
{
	LoadConfig();
}
void AppSettings::LoadConfig()
{
	appName->setText(_AppName.c_str());
	username->setText(_UserName.c_str());
	iconPath->setText(_IconPath.c_str());
	fps->setText(to_string(_FPS).c_str());
	appKey->setText(_ApiKey.c_str());
	appSecret->setText(_ApiSecret.c_str());
	windowWidth->setText(to_string(_WindowWidth).c_str());
	windowHeight->setText(to_string(_WindowHeight).c_str());
	modelDir->setText(_ModelDir.c_str());
}

ModelSettings::ModelSettings(QWidget* p)
{
	_parent = p;
	model = new QComboBox();
	lbl_model = new QLabel(QString::fromLocal8Bit("ѡ��ģ��"));
	_motionGroups = new QTreeWidget();

	_motionGroups->setHeaderLabel(QString::fromLocal8Bit("������"));
	apply = new QPushButton(QString::fromLocal8Bit("����"));
	cancel = new QPushButton(QString::fromLocal8Bit("����"));

	motionJsonPath = new QComboBox();
	motionSoundPath = new QComboBox();
	motionText = new QTextEdit();

	lbl_motionJsonPath = new QLabel(QString::fromLocal8Bit("����·��"));
	lbl_motionJsonPath->setAlignment(Qt::AlignRight);
	lbl_motionSoundPath = new QLabel(QString::fromLocal8Bit("����"));
	lbl_motionSoundPath->setAlignment(Qt::AlignRight);
	lbl_motionText = new QLabel(QString::fromLocal8Bit("�ı�"));
	lbl_motionText->setAlignment(Qt::AlignTop|Qt::AlignRight);

	addMotion = new QPushButton(QString::fromLocal8Bit("��Ӷ���"));
	deleteMotion = new QPushButton(QString::fromLocal8Bit("ɾ������"));
	changeModel = new QPushButton(QString::fromLocal8Bit("����ģ��"));

	connect(apply, SIGNAL(clicked()), SLOT(Apply()));
	connect(cancel, SIGNAL(clicked()), SLOT(Cancel()));
	grid = new QGridLayout();
	grid->addWidget(lbl_model, 0, 0, 0);
	grid->addWidget(model, 0, 1, 0);
	grid->addWidget(changeModel, 0, 2, 0);
	grid->addWidget(_motionGroups, 1, 0, 3, 2, 0);
	grid->addWidget(motionJsonPath, 1, 3, 1, 2, 0);
	grid->addWidget(motionSoundPath, 2, 3, 1, 2, 0);
	grid->addWidget(motionText, 3, 3, 1, 2, 0);
	grid->addWidget(lbl_motionJsonPath, 1, 2, 0);
	grid->addWidget(lbl_motionSoundPath, 2, 2, 0);
	grid->addWidget(lbl_motionText, 3, 2, 0);
	grid->addWidget(addMotion, 4, 0, 0);
	grid->addWidget(deleteMotion, 4, 1, 0);
	grid->addWidget(apply, 4, 3, 0);
	grid->addWidget(cancel, 4, 4, 0);
	setLayout(grid);

	connect(_motionGroups, SIGNAL(itemClicked(QTreeWidgetItem*, int)), SLOT(ShowMotionInfo(QTreeWidgetItem*, int)));
	connect(addMotion, SIGNAL(clicked()), SLOT(AddMotion()));
	connect(deleteMotion, SIGNAL(clicked()), SLOT(DeleteMotion()));

	connect(motionJsonPath, SIGNAL(currentTextChanged(const QString&)), SLOT(BindMotion(const QString&)));
	connect(motionSoundPath, SIGNAL(currentTextChanged(const QString&)), SLOT(BindSound(const QString&)));
	connect(motionText, SIGNAL(textChanged()), SLOT(BindText()));

	connect(changeModel, SIGNAL(clicked()), SLOT(UpdateModel()));
}

void ModelSettings::Apply()
{
	if (QMessageBox::question(_parent, QString::fromLocal8Bit("��������"), QString::fromLocal8Bit("�Ƿ񱣴�����?"), QMessageBox::Yes | QMessageBox::No) == QMessageBox::Yes)
	{
		ofstream ofs(string(_ModelDir).append("/").append(_ModelName).append("/").append(_ModelName).append(".model3.json"));
		ofs << _modelJson;
		ofs.close();
		LoadConfig();
		Tip::GetInstance()->Pop(_parent, "�����ɹ�!");
	}
	
}

void ModelSettings::Cancel()
{
	LoadConfig();
}

void ModelSettings::LoadConfig()
{
	_motionGroups->clear();
	motionJsonPath->clear();
	motionSoundPath->clear();
	motionText->clear();
	int i;
	int size;
	vector<std::string> _files;

	getDirNames(_ModelDir, _files);
	size = _files.size();
	model->clear();
	for (i = 0; i < size; i++)
	{
		model->addItem(_files[i].c_str());
	}
	model->setCurrentText(_ModelName.c_str());
	motionJsonPath->clear();
	_files.clear();
	getFileNames(string(_ModelDir).append("/").append(_ModelName).append("/").append("motions"), _files);
	size = _files.size();
	for (i = 0; i < size; i++)
	{
		motionJsonPath->addItem(string("motions/").append(_files[i]).c_str());
	}
	motionSoundPath->clear();
	motionJsonPath->addItem("");
	motionJsonPath->setCurrentText("");
	_files.clear();
	getFileNames(string(_ModelDir).append("/").append(_ModelName).append("/").append("sounds"), _files);
	size = _files.size();
	for (i = 0; i < size; i++)
	{
		motionSoundPath->addItem(string("sounds/").append(_files[i]).c_str());
	}
	motionSoundPath->addItem("");
	motionSoundPath->setCurrentText("");
	ifstream ifs(string(_ModelDir).append("/").append(_ModelName).append("/").append(_ModelName).append(".model3.json"));
	ifs >> _modelJson;
	ifs.close();
	Json::Value motions = _modelJson["FileReferences"]["Motions"];
	vector<const char*> groupnames = { "Morning", "Afternoon", "Evening", "Midnight", "TapHead", "TapBody", "TapSpecial", "LongSittingTip" };
	size = groupnames.size();
	QTreeWidgetItem* item;
	QTreeWidgetItem* subItem;
	int j;
	int size2;
	for (i = 0; i < size; i++)
	{
		item = new QTreeWidgetItem();
		_motionGroups->addTopLevelItem(item);
		Json::Value motionGroups = motions[groupnames[i]];
		item->setText(0, groupnames[i]);
		size2 = motionGroups.size();

		for (j = 0; j < size2; j++)
		{
			subItem = new QTreeWidgetItem();
			subItem->setText(0, string(groupnames[i]).append("_").append(to_string(j)).c_str());
			subItem->setData(1, 0, j);
			item->addChild(subItem);
		}
	}
	
}

void ModelSettings::BindMotion(const QString& x)
{
	QTreeWidgetItem* cur = _motionGroups->currentItem();
	if (cur != NULL && cur->parent() != NULL)
	{
		if (_access(QString::fromStdString(_ModelDir).append("/").append(QString::fromStdString(_ModelName)).append("/").append(motionJsonPath->currentText()).toStdString().c_str(), 0)!= -1)
		{
			if (!motionJsonPath->currentText().isEmpty())
			{
				_modelJson["FileReferences"]["Motions"][cur->parent()->text(0).toStdString()][cur->parent()->indexOfChild(cur)]["File"] = motionJsonPath->currentText().toStdString();
				Tip::GetInstance()->Pop(_parent, "���������ɹ�!");
			}
			else {
				Tip::GetInstance()->Pop(_parent, "��������Ϊ��!");
			}
		}
		else Tip::GetInstance()->Pop(_parent, "�����ļ�������!");
	}
}

void ModelSettings::BindSound(const QString& x)
{
	QTreeWidgetItem* cur = _motionGroups->currentItem();
	if (cur != NULL && cur->parent() != NULL)
	{
		_modelJson["FileReferences"]["Motions"][cur->parent()->text(0).toStdString()][cur->parent()->indexOfChild(cur)]["Sound"] = motionSoundPath->currentText().toStdString();
		Tip::GetInstance()->Pop(_parent, "��Ƶ�����ɹ�!");
	}
		
}

void ModelSettings::BindText()
{
	QTreeWidgetItem* cur = _motionGroups->currentItem();
	if (cur != NULL && cur->parent() != NULL)
	{
		_modelJson["FileReferences"]["Motions"][cur->parent()->text(0).toStdString()][cur->parent()->indexOfChild(cur)]["Text"] = motionText->toPlainText().toStdString();
		Tip::GetInstance()->Pop(_parent, "�ı������ɹ�!");
	}
		

}

void ModelSettings::AddMotion()
{
	if (_motionGroups->currentItem() == NULL)  //��ѡ��
	{
		return;
	}
	else if (_motionGroups->currentItem()->parent() == NULL)  //ѡ������������
	{
		Json::Value motion;
		motion["File"] = motionJsonPath->itemText(0).toStdString();
		motion["Sound"] = "";
		motion["Text"] = "";
		_modelJson["FileReferences"]["Motions"][_motionGroups->currentItem()->text(0).toStdString()].append(motion);

		int idx = _motionGroups->currentItem()->childCount();
		QTreeWidgetItem* subItem = new QTreeWidgetItem();
		subItem->setText(0, QString::fromStdString(_motionGroups->currentItem()->text(0).toStdString()).append("_").append(to_string(idx).c_str()));
		subItem->setData(1, 0, idx);
		_motionGroups->currentItem()->addChild(subItem);
		Tip::GetInstance()->Pop(_parent, "���������!");
	}
	else  //ѡ���Ӷ��� 
	{
		QTreeWidgetItem* p = _motionGroups->currentItem()->parent();

		Json::Value motion;
		motion["File"] = motionJsonPath->itemText(0).toStdString();
		motion["Sound"] = "";
		motion["Text"] = "";
		_modelJson["FileReferences"]["Motions"][p->text(0).toStdString()].append(motion);

		int idx = p->childCount();
		QTreeWidgetItem* subItem = new QTreeWidgetItem();
		subItem->setText(0, QString::fromStdString(p->text(0).toStdString()).append("_").append(to_string(idx).c_str()));
		subItem->setData(1, 0, idx);
		p->addChild(subItem);
		Tip::GetInstance()->Pop(_parent, "���������!");
	}
}

void ModelSettings::DeleteMotion()
{
	if (_motionGroups->currentItem() == NULL)  //��ѡ��
	{
		return;
	}
	else if (_motionGroups->currentItem()->parent() == NULL)  //ѡ������������
	{
		return;
	}
	else  //ѡ���Ӷ��� 
	{
		QTreeWidgetItem* p = _motionGroups->currentItem()->parent();
		_modelJson["FileReferences"]["Motions"][p->text(0).toStdString()].removeIndex(p->indexOfChild(_motionGroups->currentItem()), NULL);
		p->removeChild(_motionGroups->currentItem());
		int i;
		int size = p->childCount();
		for (i = 0; i < size; i++)
		{
			p->child(i)->setData(1, 0, i);
			p->child(i)->setText(0, QString(p->text(0)).append("_").append(to_string(i).c_str()));
		}
		motionJsonPath->setCurrentText("");
		motionSoundPath->setCurrentText("");
		motionText->clear();
		Tip::GetInstance()->Pop(_parent, "������ɾ��!");
	}
}

void ModelSettings::ShowMotionInfo(QTreeWidgetItem* w, int idx)
{
	if (w->parent() != NULL)
	{
		string groupname = w->parent()->text(0).toStdString();
		int idx = w->data(1, 0).toInt();
		Json::Value motion = _modelJson["FileReferences"]["Motions"][groupname][idx];


		motionJsonPath->setCurrentText(motion["File"].asCString());
		motionSoundPath->setCurrentText(motion["Sound"].isNull() ? "" : motion["Sound"].asCString());
		motionText->setText(motion["Text"].isNull() ? "" : motion["Text"].asCString());
	}
	else{
		motionJsonPath->setCurrentText("");
		motionSoundPath->setCurrentText("");
		motionText->clear();
	}
}

void ModelSettings::UpdateModel()
{
	_ModelName = model->currentText().toStdString();
	LAppLive2DManager::GetInstance()->ChangeModel(_ModelDir.c_str(), _ModelName.c_str());
	LApp::GetInstance()->SaveConfig();
	LoadConfig();
	Tip::GetInstance()->Pop(_parent, "ģ���Ѹ���");
}

ControlWidget::ControlWidget()
{
	resize(600, 400);
	setWindowFlags(Qt::Tool);
	setWindowTitle(QString::fromStdString(_AppName));
	_appSettings = new AppSettings(this);
	_modelSettings = new ModelSettings(this);
	addTab(_appSettings, QString::fromLocal8Bit("Ӧ������"));
	addTab(_modelSettings, QString::fromLocal8Bit("ģ������"));
}


void ControlWidget::Pop()
{
	_appSettings->LoadConfig();
	_modelSettings->LoadConfig();
	show();
	raise();
}

