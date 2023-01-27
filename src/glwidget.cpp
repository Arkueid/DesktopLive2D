#include "LAppDelegate.hpp"
#include "LAppLive2DManager.hpp"
#include "LAppPal.hpp"
#include "glwidget.h"
#include "LAppDefine.hpp"
#include "LAppView.hpp"
#include "LAppModel.hpp"
#include "LApp.h"
#include <QtGui/qevent.h>
#include <QtWidgets/qopenglwidget.h>
#include <QtWidgets/qsystemtrayicon.h>
#include <QtWidgets/qaction.h>
#include <QtWidgets/qmenu.h>
#include <QtCore/qtextcodec.h>
#include <QtGui/qtextoption.h>
#include <QtWidgets/qmessagebox.h>
#include <QtWidgets/qtextbrowser.h>
#include <QtCore/qpropertyanimation.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <QtWidgets/qstyle.h>
#include <unordered_map>
#include <time.h>
#include <ctime>
#include <QtGui/qstylehints.h>
#include "json/json.h"


using namespace LAppDefine;
using namespace std;


void FinishedMotion(ACubismMotion* self)
{
	if (DebugLogEnable)
	{
		LAppPal::PrintLog("Motion Finished: %x", self);
	}
}

GLWidget::GLWidget() 
{
	//����͸������
	setWindowFlag(Qt::FramelessWindowHint);
	setAttribute(Qt::WA_TranslucentBackground, true);
	
	//�Ӵ��ڣ�������������ʾͼ��
	setWindowFlag(Qt::SubWindow);

	//��¼���λ������
	mouseX = 0;
	mouseY = 0;
}

GLWidget::~GLWidget()
{

}

void GLWidget::initializeGL()
{
	LAppDelegate::GetInstance()->Initialize(this);
	LAppDelegate::GetInstance()->resize(this->width(), this->height());
}

void GLWidget::resizeGL(int w, int h)
{
	LAppDelegate::GetInstance()->resize(this->width(), this->height());
}

void GLWidget::paintGL()
{
	LAppDelegate::GetInstance()->update();
}

void GLWidget::timerEvent(QTimerEvent* e)
{
	update();
	float x, y;
	x = QCursor::pos().x() - this->x();
	y = QCursor::pos().y() - this->y();
	LAppDelegate::GetInstance()->GetView()->TransformCoordinate(&x, &y);
	bool res1 = LAppLive2DManager::GetInstance()->GetModel(0)->HitTest("Body", x, y);
	bool res2 = LAppLive2DManager::GetInstance()->GetModel(0)->HitTest("Head", x, y);
	bool res3 = LAppLive2DManager::GetInstance()->GetModel(0)->HitTest("Special", x, y);
	HWND hWnd = (HWND)(this->winId());
	if ((res1 || res2 || res3) && !_keepQuiet)
	{
		SetWindowLong(hWnd, GWL_EXSTYLE, GetWindowLongW(hWnd, GWL_EXSTYLE) & (~WS_EX_TRANSPARENT));
	}
	else
	{
		SetWindowLong(hWnd, GWL_EXSTYLE, GetWindowLongW(hWnd, GWL_EXSTYLE) | WS_EX_TRANSPARENT);
		setCursor(QCursor(Qt::PointingHandCursor));
	}
	if (_mouseTrack)
	{
		LAppLive2DManager::GetInstance()->OnDrag(x, y);
	}
	if (runFor / FPS > 3600)
	{
		LAppLive2DManager::GetInstance()->GetModel(0)->StartRandomMotion("LongSittingTip", PriorityForce, FinishedMotion);
		runFor = 0;
	}
	runFor++;
}

void GLWidget::mousePressEvent(QMouseEvent* e)
{
	LAppDelegate::GetInstance()->OnMouseCallBack(e->button(), 1);
	LAppDelegate::GetInstance()->OnMouseCallBack(e->localPos().x(), e->localPos().y());
	mouseX = e->pos().x();
	mouseY = e->pos().y();

}

void GLWidget::mouseMoveEvent(QMouseEvent* e)
{
	LAppDelegate::GetInstance()->OnMouseCallBack(e->localPos().x(), e->localPos().y());
	LAppDelegate::GetInstance()->OnMouseCallBack(e->localPos().x(), e->localPos().y());
	if (e->buttons() == Qt::RightButton)
	{
		move(x() + e->pos().x() - mouseX, y() + e->pos().y() - mouseY);
	}
}

void GLWidget::mouseDoubleClickEvent(QMouseEvent* e)
{
	LAppModel* model = LAppLive2DManager::GetInstance()->GetModel(0);
	if (model->isFinished())
	{
		model->StartRandomMotion(MotionGroupIdle, PriorityIdle, FinishedMotion);
	}
}

void GLWidget::mouseReleaseEvent(QMouseEvent* e)
{
	LAppDelegate::GetInstance()->OnMouseCallBack(e->button(), 0);
	LAppDelegate::GetInstance()->OnMouseCallBack(e->localPos().x(), e->localPos().y());
}

void GLWidget::keepQuiet(bool on)
{
	_keepQuiet = on;
}

void GLWidget::keepMouseTrack(bool on)
{
	_mouseTrack = on;
	if (!on)
	{
		LAppLive2DManager::GetInstance()->OnDrag(0.0f, 0.0f);
	}
}

void GLWidget::trayIconOnActivated(QSystemTrayIcon::ActivationReason reason)
{
	if (reason == QSystemTrayIcon::DoubleClick)
	{
		// �����ƶ����
		this->setWindowFlag(Qt::WindowStaysOnTopHint, true);
		show();
		this->setWindowFlag(Qt::WindowStaysOnTopHint, false);
		show();
		QTextCodec* codec = QTextCodec::codecForName("gb2312");
		act_hide->setText(codec->toUnicode("����"));
		
	}
	else  if (reason == QSystemTrayIcon::Trigger)
	{
	}
	else if (reason == QSystemTrayIcon::Context)
	{
		showRightMenu();
	}
}

void GLWidget::showRightMenu()
{
	int mX = QCursor::pos().x() + 20;
	int mY = QCursor::pos().y() - rightMenu->height() - 10;
	rightMenu->move(mX, mY);
	rightMenu->show();

}

void GLWidget::quitOnTriggered()
{
	Release();
	LApp::GetInstance()->Release();
}

void GLWidget::Release()
{
	saveConfig();
	trayIcon->hide();
	trayIcon->deleteLater();
	for each (QAction * act in rightMenu->actions())
	{
		act->deleteLater();
	}
	rightMenu->deleteLater();
	_dialog->deleteLater();
	close();
}

void GLWidget::hideOnTriggered()
{
	QTextCodec* codec = QTextCodec::codecForName("gb2312");
	if (act_hide->text() == codec->toUnicode("����"))
	{
		this->setVisible(false);
		act_hide->setText(codec->toUnicode("��ʾ"));
	}
	else 
	{
		this->setVisible(true);
		act_hide->setText(codec->toUnicode("����"));
	}
}
void GLWidget::keepMouseTrackOnTriggered()
{
	QTextCodec* codec = QTextCodec::codecForName("gb2312");
	if (act_keepMouseTrack->text() == codec->toUnicode("�ر����׷��"))
	{
		keepMouseTrack(false);
		act_keepMouseTrack->setText(codec->toUnicode("�������׷��"));
	}
	else
	{
		keepMouseTrack(true);
		act_keepMouseTrack->setText(codec->toUnicode("�ر����׷��"));
	}
}
void GLWidget::keepQuietOnTriggered()
{
	QTextCodec* codec = QTextCodec::codecForName("gb2312");
	if (act_keepQuiet->text() == codec->toUnicode("���������"))
	{
		keepQuiet(true);
		act_keepQuiet->setText(codec->toUnicode("�ر������"));
	}
	else
	{
		keepQuiet(false);
		act_keepQuiet->setText(codec->toUnicode("���������"));
	}
}

void GLWidget::stayOnTopOnTriggered()
{
	QTextCodec* codec = QTextCodec::codecForName("gb2312");
	if (act_stayOnTop->text() == codec->toUnicode("�����ö���ʾ"))
	{
		stayOnTop(true);
		act_stayOnTop->setText(codec->toUnicode("�ر��ö���ʾ"));
	}
	else
	{
		stayOnTop(false);
		act_stayOnTop->setText(codec->toUnicode("�����ö���ʾ"));
	}
}

void GLWidget::setNoSoundOnTriggered()
{
	QTextCodec* codec = QTextCodec::codecForName("gb2312");
	if (act_setNoSound->text() == codec->toUnicode("��������"))
	{
		setNoSound(true);
		act_setNoSound->setText(codec->toUnicode("�رվ���"));
	}
	else
	{
		setNoSound(false);
		act_setNoSound->setText(codec->toUnicode("��������"));
	}
}

void GLWidget::setShowTextOnTriggered()
{
	QTextCodec* codec = QTextCodec::codecForName("gb2312");
	if (act_setShowText->text() == codec->toUnicode("�����ı���ʾ"))
	{
		setShowText(true);
		act_setShowText->setText(codec->toUnicode("�ر��ı���ʾ"));
	}
	else
	{
		setShowText(false);
		act_setShowText->setText(codec->toUnicode("�����ı���ʾ"));
	}
}

void GLWidget::Run()
{
	srand((unsigned)time(NULL));
	trayIcon->show();
	show();
	_dialog->raise();

}

#pragma region ���������ļ�
void GLWidget::loadConfig()
{
	resize(LAppConfig::_WindowWidth, LAppConfig::_WindowHeight);
	move(LAppConfig::_LastPosX, LAppConfig::_LastPosY);
	this->FPS = (int)LAppConfig::_FPS;
	_mouseTrack = LAppConfig::_MouseTrack;
	_keepQuiet = LAppConfig::_KeepQuiet;
	_onTop = LAppConfig::_StayOnTop;
	_showText = LAppConfig::_ShowText;
	_noSound = LAppConfig::_NoSound;
	setWindowFlag(Qt::WindowStaysOnTopHint, _onTop);
	//����ϵͳ����
	QTextCodec* codec = QTextCodec::codecForName("gb2312");
	this->trayIcon = new QSystemTrayIcon(this);
	ifstream f(LAppConfig::_IconPath, ios::binary);
	if (!f.good())
	{
		trayIcon->setIcon(QApplication::style()->standardIcon(QStyle::SP_VistaShield));
	}
	else
	{
		trayIcon->setIcon(QIcon(LAppConfig::_IconPath.c_str()));
	}
	f.close();
	QTextCodec* codec0 = QTextCodec::codecForName("utf-8");
	trayIcon->setToolTip(codec0->toUnicode(LAppConfig::_WindowTitle.c_str()));
	connect(trayIcon, SIGNAL(activated(QSystemTrayIcon::ActivationReason)), this, SLOT(trayIconOnActivated(QSystemTrayIcon::ActivationReason)));

	//�Ҽ��˵�
	rightMenu = new QMenu(this);
	act_quit = new QAction(codec->toUnicode("�˳�"));
	act_hide = new QAction(codec->toUnicode("����"));
	act_keepMouseTrack = new QAction(codec->toUnicode(_mouseTrack ? "�ر����׷��" : "�������׷��"));
	act_keepQuiet = new QAction(codec->toUnicode(_keepQuiet ? "�ر������" : "���������"));
	act_stayOnTop = new QAction(codec->toUnicode(_onTop ? "�ر��ö���ʾ" : "�����ö���ʾ"));
	act_setNoSound = new QAction(codec->toUnicode(_noSound ? "�رվ���" : "��������"));
	act_setShowText = new QAction(codec->toUnicode(_showText ? "�ر��ı���ʾ" : "�����ı���ʾ"));

	//�Ҽ��˵��ź�
	connect(act_quit, SIGNAL(triggered()), SLOT(quitOnTriggered()));
	connect(act_hide, SIGNAL(triggered()), SLOT(hideOnTriggered()));
	connect(act_keepMouseTrack, SIGNAL(triggered()), SLOT(keepMouseTrackOnTriggered()));
	connect(act_keepQuiet, SIGNAL(triggered()), SLOT(keepQuietOnTriggered()));
	connect(act_stayOnTop, SIGNAL(triggered()), SLOT(stayOnTopOnTriggered()));
	connect(act_setNoSound, SIGNAL(triggered()), SLOT(setNoSoundOnTriggered()));
	connect(act_setShowText, SIGNAL(triggered()), SLOT(setShowTextOnTriggered()));

	rightMenu->addActions({ act_quit, act_hide, act_keepMouseTrack, act_keepQuiet, act_stayOnTop, act_setNoSound, act_setShowText });
	startTimer(1000 / FPS);
	_dialog = new Dialog();

}
#pragma endregion

#pragma region ���������ļ�
void GLWidget::saveConfig()
{
	LApp::GetInstance()->SaveConfig();
}
#pragma endregion

Dialog::Dialog()
{
	_textBrowser = new QTextBrowser(this);
	const char* styleSheet = LAppConfig::_DialogStyleSheet.c_str();
	setStyleSheet(styleSheet);
	int w = LAppConfig::_DialogWidth;
	int h = LAppConfig::_DialogHeight;
	resize(w, h);
	_textBrowser->resize(w, h);
	setWindowFlags(Qt::SubWindow | Qt::FramelessWindowHint);
	setAttribute(Qt::WA_TranslucentBackground);
	_textBrowser->setAttribute(Qt::WA_TransparentForMouseEvents);
	animation = new QPropertyAnimation(this, NULL);
	animation->setStartValue(0);
	animation->setEndValue(0);
	animation->setDuration(LAppConfig::_TextFadeOutTime * 1000);
	connect(animation, SIGNAL(finished()), this, SLOT(close()));
}

void Dialog::pop(const char* text)
{
	animation->stop();
	_textBrowser->clear();
	QTextCodec* codec = QTextCodec::codecForName("utf-8");
	GLWidget* win = LApp::GetInstance()->GetWindow();
	move(win->x() + (win->width() - width()) / 2 , win->y() + (win->height() - height()) * 2 / 3);
	_textBrowser->setText(codec->toUnicode(text));
	setWindowFlag(Qt::WindowStaysOnTopHint, LApp::GetInstance()->GetWindow()->OnTop());
	show();
	raise();
	animation->start();
}
void Dialog::Release()
{
	_textBrowser->deleteLater();
}

void Dialog::mouseReleaseEvent(QMouseEvent* e)
{
	close();
}

void GLWidget::showDialog(const char* text)
{
	_dialog->pop(text);
}

void GLWidget::stayOnTop(bool on)
{
	_onTop = on;
	setWindowFlag(Qt::WindowStaysOnTopHint, on);
	show();
}

void GLWidget::setNoSound(bool on)
{
	_noSound = on;
}

void GLWidget::setShowText(bool on)
{
	_showText = on;
}
