from framework.runtime.core.model.model_manager import ModelManager

if __name__ == '__main__':
    modelManager = ModelManager()
    modelManager.initialize("../../Resources")
    print([str(i) for i in modelManager.modelInfoList])