from ..models.LLMTemplate import LLMTemplate
from init.database import db
from flask import jsonify


class CloudLLMService:
    @staticmethod
    def CreateCloudLLM(cloudData):
        try:
            cloudDatas = {
                "name": cloudData.get("name"),
                "description": cloudData.get("description"),
                "docker_image_url": cloudData.get("docker_image_url"),
                "type": cloudData.get("type", "Cloud_LLM"),
                "version": cloudData.get("version"),
                "tags": cloudData.get("tags"),            
            }
            newCloudLLM = LLMTemplate(**cloudDatas)
            db.session.add(newCloudLLM)
            db.session.commit()
            return jsonify({"message": "CloudLLM created successfully"}),200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def getCloudLLM(cloudllm_id):
        cloudLLM = LLMTemplate.query.get(cloudllm_id)
        if cloudLLM is None:
            return jsonify({"message": f"No CloudLLM found with id: {cloudllm_id}"})
        else:
            return jsonify(cloudLLM.to_dict())

    @staticmethod
    def getAllCloudLLMs():
        return jsonify([cloudLLM.to_dict() for cloudLLM in LLMTemplate.query.all()])

    @staticmethod
    def deleteCloudLLM(cloudllm_id):
        cloudLLM = LLMTemplate.query.get(cloudllm_id)
        if cloudLLM is None:
            return jsonify({"message": f"No CloudLLM found with id: {cloudllm_id}"})
        else:
            db.session.delete(cloudLLM)
            db.session.commit()
            return jsonify(
                {"message": f"CloudLLM with id: {cloudllm_id} deleted successfully"}
            )

    @staticmethod
    def changeCloudLLMStatus(cloudllm_id, status):
        cloudLLM = LLMTemplate.query.get(cloudllm_id)
        if cloudLLM is None:
            return jsonify({"message": f"No CloudLLM found with id: {cloudllm_id}"})
        else:
            cloudLLM.is_active = status
            db.session.commit()
            return jsonify(
                {
                    "message": f"CloudLLM with id: {cloudllm_id} status changed successfully"
                }
            )
