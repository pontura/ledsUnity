from time import sleep,time

class fps:    
    fps = 0
    fps_count = 0    
    start_time = time()
    lastTime = start_time
    def Update(self):
        t = time()
        if (t-self.start_time) > 1:
            self.fps = self.fps_count
            self.fps_count = 1
            self.start_time = t
            print("FPS:",self.fps)
        else:
            self.fps_count += 1
        
        dif = t - self.lastTime
        self.lastTime = t
        return dif

