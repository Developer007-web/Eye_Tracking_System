import cv2
import mediapipe as mp
import csv
import time
import matplotlib.pyplot as plt

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Start webcam
cap = cv2.VideoCapture(0)

# Get video properties
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Setup video writer
timestamp = int(time.time())
out = cv2.VideoWriter(f'eye_tracking_{timestamp}.avi',
                      cv2.VideoWriter_fourcc(*'XVID'), 20,
                      (frame_width, frame_height))

# Setup CSV
csv_file = open(f'eye_tracking_{timestamp}.csv', mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Frame', 'Right_Iris_X', 'Right_Iris_Y', 'Left_Iris_X', 'Left_Iris_Y'])

# For plotting
right_x_vals, right_y_vals = [], []
left_x_vals, left_y_vals = [], []
frame_nums = []

plt.ion()
fig, ax = plt.subplots()
right_scatter = ax.scatter([], [], c='g', label='Right Eye')
left_scatter = ax.scatter([], [], c='r', label='Left Eye')
ax.set_xlim(0, frame_width)
ax.set_ylim(frame_height, 0)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.legend()

frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    rx, ry, lx, ly = None, None, None, None

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Right iris
            right_iris = face_landmarks.landmark[474]
            rx, ry = int(right_iris.x * w), int(right_iris.y * h)

            # Left iris
            left_iris = face_landmarks.landmark[469]
            lx, ly = int(left_iris.x * w), int(left_iris.y * h)

            # Draw on frame
            cv2.circle(frame, (rx, ry), 3, (0, 255, 0), -1)
            cv2.circle(frame, (lx, ly), 3, (0, 0, 255), -1)
            cv2.putText(frame, f'R:({rx},{ry})', (rx + 10, ry), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.putText(frame, f'L:({lx},{ly})', (lx + 10, ly), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # Save data
    frame_count += 1
    csv_writer.writerow([frame_count, rx, ry, lx, ly])

    if rx and ry and lx and ly:
        right_x_vals.append(rx)
        right_y_vals.append(ry)
        left_x_vals.append(lx)
        left_y_vals.append(ly)
        frame_nums.append(frame_count)

        # Update plot
        right_scatter.set_offsets(list(zip(right_x_vals, right_y_vals)))
        left_scatter.set_offsets(list(zip(left_x_vals, left_y_vals)))
        plt.pause(0.001)

    # Show and save video
    cv2.imshow("Eye Tracking", frame)
    out.write(frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

# Cleanup
cap.release()
out.release()
csv_file.close()
cv2.destroyAllWindows()
plt.ioff()
plt.show()
