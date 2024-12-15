from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

app = Ursina()

Entity.default_shader = lit_with_shadows_shader

DirectionalLight(y=2,rotation=(45,45,0))

Sky()

ground = Entity(model='plane',collider='box',scale=64,texture='grass')

for i in range(16):
    Entity(model='cube',scale=2,texture='brick',
           texture_scale=(1,2),
           x=random.uniform(-8,8),
           z=random.uniform(-8,8)+8,
           collider='box',
           scale_y=random.uniform(2,3),
           origin_y=-0.5)
    
    editor_camera = EditorCamera(enabled = False)

def input_pause(key):
    if key == 'tab':
        editor_camera.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        player.visible_self = editor_camera.enabled
        editor_camera.position = player.position
        if editor_camera.enabled:
            camera.rotation_x = 0
            camera.rotation_y = 0
            camera.position = (0,2,0)
            camera.fov = 90
        else:
            camera.rotation_x = 0
            camera.rotation_y = 0
            camera.position = (0,10,0)
            camera.fov = 60


pause_handler = Entity(input=input_pause)

player = FirstPersonController(model='cube',color=color.orange,z=-10,origin_y=-0.5,speed=8,collider='box')

gun = Entity(model='cube',parent=camera,scale=(0.3,0.2,1),position=(0.5,-0.25,0.5),color=color.red,on_cooldown=False)
gun.flash = Entity(parent=gun,model='quad',z=1,color=color.yellow,enabled=False)

def shoot():
    if not gun.on_cooldown:
        #print("shooting")
        gun.on_cooldown = True
        gun.flash.enabled = True
        from ursina.prefabs.ursfx import ursfx
        ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)], volume=0.5, wave='noise',
              pitch=random.uniform(-13,12), pitch_change=-12, speed=3.0)
        invoke(gun.flash.disable, delay = 0.15)
        invoke(setattr,gun,'on_cooldown',False,delay = 0.15)
        if mouse.hovered_entity and hasattr(mouse.hovered_entity,'hp'):
            mouse.hovered_entity.blink(color.red)
            mouse.hovered_entity.hp -= 10
            if mouse.hovered_entity.hp <=0 :
                destroy(mouse.hovered_entity)
                Enemy(x = random.randint(-32,32))
            mouse.hovered_entity.health_bar.scale_x = mouse.hovered_entity.hp/mouse.hovered_entity.max_hp * 1.5

def update():
    if held_keys['left mouse']:
        shoot()

class Enemy(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities,model='cube',
                         collider='box',
                         scale_y=2,origin_y=-0.5,
                          color=color.light_gray, **kwargs)
        self.health_bar = Entity(parent=self,model='cube',color=color.red,y=1.2,
                                 scale=(1.5,0.1,0.1))
        self.max_hp = 100
        self.hp = self.max_hp

    def update(self):
        self.look_at_2d(player.position,'y')

        hit_info = raycast(self.position+Vec3(0,1,0),self.forward,30,ignore=(self,),debug=False)
        if hit_info.entity == player:
            if distance_xz(self.position,player.position)>2:
                self.position = self.position + self.forward*time.dt*5

for i in range(4):
    Enemy(x=i*4)

app.run()