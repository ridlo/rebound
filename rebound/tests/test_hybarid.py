import rebound
import unittest
import os
import rebound.data as data

class TestHybarid(unittest.TestCase):
    
    def test_no_close_encounter(self):
        sim = rebound.Simulation()
        sim.add(m=1.)
        sim.add(m=1.e-3, a=1.523,e=0.0146,f=0.24)
        sim.add(m=1.e-3, a=2.423523,e=0.01246,f=0.324)
        sim.integrator = "hybarid"
        P = sim.particles[1].P
        sim.dt = 1e-4*P
        sim.integrate(P)
        x_hybarid = sim.particles[1].x
        
        sim = rebound.Simulation()
        sim.add(m=1.)
        sim.add(m=1.e-3, a=1.523,e=0.0146,f=0.24)
        sim.add(m=1.e-3, a=2.423523,e=0.01246,f=0.324)
        sim.integrator = "whfast"
        P = sim.particles[1].P
        sim.dt = 1e-4*P
        sim.integrate(P)
        x_whfast = sim.particles[1].x

        self.assertEqual(x_hybarid,x_whfast)

    #This fails when Ari tries to run it on his machine.
    def test_close_encounter(self):
        sim = rebound.Simulation()
        sim.add(m=1.)
        print(rebound.__build__)
        sim.add(m=1.e-3, a=1.523,e=0.0146,f=0.24)
        rh = sim.particles[1].a*pow(sim.particles[1].m/(3.*sim.particles[0].m),1./3)
        dust = rebound.Particle(simulation=sim, primary=sim.particles[1], a=0.25*rh, e=0.000123, f=2.3, m=1e-8)
        sim.add(dust)
        sim.integrator = "hybarid"
        sim.gravity = "basic"
        sim.ri_hybarid.switch_radius = 2.
        P = sim.particles[1].P
        sim.dt = 1e-4*P
        for i in range(1000):
            sim.step()
        x_hybarid = sim.particles[1].x
        
        sim = rebound.Simulation()
        sim.add(m=1.)
        sim.add(m=1.e-3, a=1.523,e=0.0146,f=0.24)
        dust = rebound.Particle(simulation=sim, primary=sim.particles[1], a=0.25*rh, e=0.000123, f=2.3, m=1e-8)
        sim.add(dust)
        sim.integrator = "ias15"
        sim.gravity = "basic"
        P = sim.particles[1].P
        dt0 = 1e-4*P
        sim.dt = dt0
        t = 0.
        for i in range(1000):
            t += dt0/2.
            t += dt0/2.
            sim.integrate(t)
        x_ias15 = sim.particles[1].x

        print(abs((x_hybarid-x_ias15)/x_ias15))
        self.assertEqual(x_hybarid,x_ias15)

'''
    def test_collision(self):
        sim = rebound.Simulation()
        sim.add(m=1.)
        sim.add(m=1e-5,a=0.5,e=0.1,r=1.6e-4)
        sim.add(m=1e-9,a=sim.particles[1].x+0.1,e=0.4,f=-0.94,r=4e-5)
        sim.N_active = 2
        sim.move_to_com()

        sim.integrator = "hybarid"
        sim.gravity = "basic"
        sim.ri_hybarid.switch_radius = 6.
        sim.dt = 0.001
        sim.testparticle_type = 1
        sim.collision = "direct"
        sim.collision_resolve = "merge"
        sim.integrate(5)
'''

if __name__ == "__main__":
    unittest.main()

