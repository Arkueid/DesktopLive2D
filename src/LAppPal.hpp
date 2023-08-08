/**
 * Copyright(c) Live2D Inc. All rights reserved.
 *
 * Use of this source code is governed by the Live2D Open Software license
 * that can be found at https://www.live2d.com/eula/live2d-open-software-license-agreement_en.html.
 */

#pragma once

#include <CubismFramework.hpp>
#include <string>

/**
* @brief �ץ�åȥե��`������C�ܤ���󻯤��� Cubism Platform Abstraction Layer.
*
* �ե������i���z�ߤ�r��ȡ�õȤΥץ�åȥե��`������椹���v����ޤȤ��
*
*/
class LAppPal
{
public:
    /**
    * @brief �ե������Х��ȥǩ`���Ȥ����i���z��
    *
    * �ե������Х��ȥǩ`���Ȥ����i���z��
    *
    * @param[in]   filePath    �i���z�ߌ���ե�����Υѥ�
    * @param[out]  outSize     �ե����륵����
    * @return                  �Х��ȥǩ`��
    */
    static Csm::csmByte* LoadFileAsBytes(const std::string filePath, Csm::csmSizeInt* outSize);


    /**
    * @brief �Х��ȥǩ`�����Ť���
    *
    * �Х��ȥǩ`�����Ť���
    *
    * @param[in]   byteData    ��Ť������Х��ȥǩ`��
    */
    static void ReleaseBytes(Csm::csmByte* byteData);

    /**
    * @biref   �ǥ륿�r�g��ǰ�إե�`��Ȥβ�֣���ȡ�ä���
    *
    * @return  �ǥ륿�r�g[ms]
    *
    */
    static Csm::csmFloat32 GetDeltaTime();

    static void UpdateTime();

    /**
    * @brief �����������
    *
    * �����������
    *
    * @param[in]   format  ��ʽ��������
    * @param[in]   ...     (�ɉ��L����)������
    *
    */
    static void PrintLog(const Csm::csmChar* format, ...);

    /**
    * @brief ��å��`�����������
    *
    * ��å��`�����������
    *
    * @param[in]   message  ������
    *
    */
    static void PrintMessage(const Csm::csmChar* message);

private:
    static double s_currentFrame;
    static double s_lastFrame;
    static double s_deltaTime;
};

