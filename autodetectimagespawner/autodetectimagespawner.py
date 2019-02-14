from dockerspawner import DockerSpawner
from traitlets import default, Unicode
from tornado.concurrent import Future
import re

class AutoDetectImageSpawner(DockerSpawner):
    
    image_pattern = Unicode(
        "jupyter/(.+)-notebook:(.+)",
        help="""The pattern to find images available in docker images stack
        Default pattern suitable to jupyter/docker-stacks image
        see https://github.com/jupyter/docker-stacks
        """,
        config=True
    )

    def _get_image_list(self):
        regex = re.compile(self.image_pattern)
        image_list = [
            s for i in self.client.images() for s in i['RepoTags'] if regex.match(s)
        ]
        return image_list

    def callable_options_form(self, spawner):
        image_list = self._get_image_list()
        if len(image_list) <= 1:
            return ''
        option_t = '<option value="{image}">{image}</option>'
        options = [option_t.format(image=image) for image in image_list]
        return """
        <label for="image">Select an image:</label>
        <select class="form-control" name="image" required autofocus>
        {options}
        </select>
        """.format(options=options)
    
    # return a callable to enable refreshing
    @default('options_form')
    def _options_form(self):
        return self.callable_options_form
    
    def options_from_form(self, formdata):
        options = {}
        if 'image' in formdata:
            options['image'] = formdata['image'][0]
        return options
 
    def start(self, image=None, extra_create_kwargs=None, extra_host_config=None):  
        image_option = self.user_options.get('image')
        if image_option:
            self.image = image_option
        return super(AutoDetectImageSpawner, self).start()
