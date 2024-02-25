from flask import Flask, render_template, Response, jsonify
from webcamtest import pose_estimate,pose_estimate_secure
import mediapipe as mp
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(1)

app.debug = True


@app.route('/')
def login_page():
    print('someone on page')
    return render_template('login.html')


@app.route('/loggedin')
def loggedin():
    return render_template('home.html')

@app.route('/stream1')
def stream():
    print('stream')
    return render_template('stream.html')
# @app.route('/video-security-on')
# def video():
#     secure = True
#     # print('reached')
#     mp_pose = mp.solutions.pose
#     pose = mp_pose.Pose()
#     # print('video')
#     return Response(generate_frames_secure(mp_pose,pose,secure),mimetype='multipart/x-mixed-replace;boundary=frame')

@app.route('/video')
def video():
    # print('reached')
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    # print('video')
    return Response(generate_frames(mp_pose,pose),mimetype='multipart/x-mixed-replace;boundary=frame')


def generate_frames(mp_pose,pose):
    while True:

        returning,frame = camera.read()
        
        if not returning:
            print('no stream')
            break
        else:
            frame = pose_estimate(mp_pose=mp_pose,pose=pose,frame=frame)
            ret,buffer = cv2.imencode('.jpg',frame)

           
            
            frame = buffer.tobytes()

        # return frame
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
# def generate_frames_secure(mp_pose,pose, secure):
#     while True:

#         returning,frame = camera.read()
        
#         if not returning:
#             print('no stream')
#             break
#         else:
#             frame = pose_estimate_secure(mp_pose=mp_pose,pose=pose,frame=frame,secure=secure)
#             if str(type(frame))=='<class \'str\'>':
                
#             ret,buffer = cv2.imencode('.jpg',frame)

           
            
#             frame = buffer.tobytes()

#         # return frame
#         yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':

    app.run(host = '0.0.0.0', port = 80,debug=True)

    