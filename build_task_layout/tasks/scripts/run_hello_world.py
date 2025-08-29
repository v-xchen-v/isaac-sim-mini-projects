from build_task_layout.tasks.hello_world.task import HelloWorldTask
import time

task = HelloWorldTask("build_task_layout/tasks/hello_world/layout.yaml")
task.set_up_scene()
for t in range(200):
    print(task.get_observations())
    
    # step the simulation, both rendering and physics
    task.layout_builder.my_world.step(render=True) # without this line, the window will still pop up, but nothing will be rendered.
    
    time.sleep(0.02)