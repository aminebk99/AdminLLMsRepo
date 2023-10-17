from ..services.cloudllm_service import CloudLLMService

class CloudLLMController:

    @staticmethod
    def getCloudLLM(cloudllm_id):
        return CloudLLMService.getCloudLLM(cloudllm_id)
    
    @staticmethod
    def getAllCloudLLMs():
        return CloudLLMService.getAllCloudLLMs()
    
    @staticmethod
    def deleteCloudLLM(cloudllm_id):
        return CloudLLMService.deleteCloudLLM(cloudllm_id)
    
    @staticmethod
    def changeCloudLLMStatus(cloudllm_id, status):
        return CloudLLMService.changeCloudLLMStatus(cloudllm_id, status)