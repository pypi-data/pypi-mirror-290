class Prompt:
    def __init__(self, id, key, title, prompt, version):
        self.id = id
        self.key = key
        self.title = title
        self.prompt = prompt
        self.endpoint_url = None
        self.version = version
        
    def __repr__(self):
        return (
            f"<Prompt(id={self.id!r}, key={self.key!r}, "
            f"title={self.title!r}, prompt={self.prompt[:30]!r}, "
            f"version={self.version!r})>"
        )
    
    def deploy(self, client) -> dict:
        return client.deploy_prompt(self)
    
    def undeploy(self, client) -> dict:
        return client.undeploy_prompt(self)
    
    def run(self, client, input_data):
        return client.create_completion(self, input_data)
    
    def list_versions(self, client):
        return client.list_versions(self)
    
    def save(self, client):
        response = client.uptate_prompt(self)
        self.id = response.get("id")
        return self
    
    def to_dict(self):
        return {
            "key": self.key,
            "title": self.title,
            "prompt": self.prompt,
        }