/*���������
*/

#include "ChatWidget.h"
#include "LAppLive2DManager.hpp"
#include "LAppModel.hpp"
#include "NetworkUtils.h"
#include "LApp.h"
#include <QtGui/qevent.h>
#include <QtGui/qpainter.h>
#include <QtGui/qclipboard.h>
#include <QtGui/qguiapplication.h>
#include <QtGui/qfontmetrics.h>
#include <QtCore/qdatetime.h>
#include <QtCore/qfile.h>
#include <io.h>
#include <QtCore/qdir.h>
#include <iostream>
#include <thread>

using namespace std;

ConversationWidget::ConversationWidget()
{
	//�ö��ޱ߿�
	setWindowFlags(Qt::Tool | Qt::FramelessWindowHint|Qt::WindowStaysOnTopHint);
	//͸������
	setAttribute(Qt::WA_TranslucentBackground);
	//��С
	setFixedSize(410, 50);
	_font.setFamily(QString::fromUtf8(LAppConfig::_ChatWidgetFontFamily.c_str()));
	_font.setPointSizeF(LAppConfig::_ChatWidgetFontSize);
	LAppConfig::_WaitChatResponse = false;
	_frame = new QFrame(this);
	_frame->setFixedSize(400, 50);

	inputArea = new QLineEdit();
	inputArea->setFont(_font);
	inputArea->setPlaceholderText(QString::fromLocal8Bit("prompt..."));
	inputArea->setStyleSheet(
		QString("QLineEdit {background-color: rgba(0, 0, 0, 0); color: ").append(LAppConfig::_ChatWidgetFontColor.c_str()).append("; border: none; }")
	);
	_frame->setObjectName("ChatWidget");
	_frame->setStyleSheet(
		QString("QScrollBar:vertical{width: 8px;background: #DDD;border: none}"
			"QScrollBar::handle:vertical{background: #AAA;}"
			"QScrollBar::handle:vertical:hover{background: #888;}"
			"QWidget#ChatWidget{background-color: ").append(LAppConfig::_ChatWidgetBackgroundColor.c_str()).append("; border-radius: 10px}")
	);
	_Send = new QPushButton();
	_Send->setStyleSheet(QString("QPushButton {border-image: url(").append(LAppConfig::_ModelDir.c_str()).append("/send.png); } QPushButton:pressed{border-image: url(").append(LAppConfig::_ModelDir.c_str()).append("/send_active.png)}"
							"QPushButton:hover{width: 30; height: 30;}"));
	_Send->setFixedSize(20, 20);
	grid = new QGridLayout();
	grid->addWidget(inputArea, 0, 0, 1, 4);
	grid->addWidget(_Send, 0, 4, 1, 1);
	_frame->setLayout(grid);
	connect(_Send, SIGNAL(clicked()), SLOT(SendRequest()));
	mouseX = 0;
	mouseY = 0;
}

void ConversationWidget::Release()
{
	_Send->deleteLater();
	grid->deleteLater();
	inputArea->deleteLater();
	close();
}

void ConversationWidget::keyPressEvent(QKeyEvent* e) {
	if (e->key() == Qt::Key_Escape) {
		close();
	}
	else if (e->key() == Qt::Key_Return) {
		SendRequest();
	}
}

void ConversationWidget::mousePressEvent(QMouseEvent* e)
{
	mouseX = e->pos().x();
	mouseY = e->pos().y();
}

void ConversationWidget::mouseMoveEvent(QMouseEvent* e)
{
	if (e->buttons() == Qt::RightButton)
	{
		move(x() + e->pos().x() - mouseX, y() + e->pos().y() - mouseY);
	}
}

//�ƶ�����ɫλ��
void ConversationWidget::AttachToCharacter()
{
	GLWidget* win = LApp::GetInstance()->GetWindow();
	move(win->x() + (win->width() - width()) / 2, win->y() + (win->height() - height()) * 2 / 3);
}

//����
void ConversationWidget::getInput()
{
	_msg.clear();
	inputArea->clear();
	AttachToCharacter();
	show();
	//���������������룬����Ҫ���������setFocus������
	inputArea->activateWindow();
	inputArea->setFocus();
}


//���������ı����ͺͽ���
void ConversationWidget::ProcessNetworkResponse()
{
	inputArea->setPlaceholderText("waiting...");
	LAppConfig::_WaitChatResponse = true;
	GLWidget* win = LApp::GetInstance()->GetWindow();
	string x = _msg.toUtf8();
	
	LApp::GetInstance()->GetWindow()->GetDialog()->WaitChatResponse();
	string text, soundPath;
	if (LAppConfig::_CustomChatServerOn)
	{
		ChatAPI::Chat(x, text, soundPath);
	}
	else {
		ChatAPI::AskMlyai(x, text);
	}
	QDir dir(LAppConfig::_ChatSavePath.c_str());
	if (!dir.exists())
	{
		dir.mkpath(".");
	}
	LAppLive2DManager::GetInstance()->GetModel(0)->Speak(text.c_str(), soundPath.c_str());
	QDateTime date = QDateTime::currentDateTime();
	QFile f(string(LAppConfig::_ChatSavePath).append("/").append(date.toString("yyyy-MM-dd").toStdString()).append(".txt").c_str());
	f.open(QIODevice::Append);
	f.write(date.toString("[yyyy-MM-dd hh:mm:ss]\n").toStdString().c_str());
	f.write(LAppConfig::_UserName.c_str());
	f.write(": ");
	f.write(_msg.toUtf8().toStdString().c_str());
	f.write("\n");
	f.write(QString(LAppConfig::_AppName.c_str()).append(": ").toUtf8().toStdString().c_str());
	f.write(QString::fromUtf8(text.c_str()).toUtf8().toStdString().c_str());
	f.write("\n");
	f.close();
	LAppConfig::_WaitChatResponse = false;
	inputArea->setPlaceholderText("prompt...");
}

//���������¼������������뷨����
void ConversationWidget::SendRequest()
{
	if (inputArea->text().isEmpty()) close();
	if (LAppConfig::_WaitChatResponse) return;
	else
	{
		if (inputArea->text().isEmpty()) return;
		_msg = inputArea->text();
		inputArea->clear();
		if (!LAppConfig::_WaitChatResponse) 
		{
			PlaySound(NULL, NULL, SND_FILENAME | SND_ASYNC);   //ֹͣ��ǰ����
			LAppLive2DManager::GetInstance()->GetModel(0)->StopLipSync();  //ֹͣ����ͬ��
			std::thread(&ConversationWidget::ProcessNetworkResponse, this).detach();  //�����̷߳��������ı�
		}
	}
}