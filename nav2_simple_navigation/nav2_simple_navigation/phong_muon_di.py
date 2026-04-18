import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
import math


def create_pose(nav, x, y, yaw):
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = nav.get_clock().now().to_msg()

    pose.pose.position.x = float(x)
    pose.pose.position.y = float(y)

    pose.pose.orientation.z = math.sin(yaw / 2.0)
    pose.pose.orientation.w = math.cos(yaw / 2.0)

    return pose


# OFFSET_X = 0.8 # toa do ban dau tien cua robot khac voi toa do ban dau tren map
# OFFSET_Y = 0.8

def go(nav, x, y, yaw, offset_x, offset_y):
    # 👉 trừ offset tại đây
    x -= offset_x
    y -= offset_y

    goal = create_pose(nav, x, y, yaw)
    nav.goToPose(goal)

    while not nav.isTaskComplete():
        pass


def optimize_path(nav, all_points, selected_indices):
    import itertools, math

    indices = [0] + [i for i in selected_indices if i != 0]

    ox, oy = all_points[0][0], all_points[0][1]

    def mk_pose(p):
        x, y, yaw = p
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = nav.get_clock().now().to_msg()
        pose.pose.position.x = x - ox
        pose.pose.position.y = y - oy
        pose.pose.orientation.z = math.sin(yaw/2)
        pose.pose.orientation.w = math.cos(yaw/2)
        return pose

    cache = {}

    def dist(p1, p2):
        key = (p1, p2)
        if key in cache:
            return cache[key]

        start = mk_pose(p1)
        goal = mk_pose(p2)

        path = nav.getPath(start, goal, use_start=True)

        if not path or len(path.poses) == 0:
            cache[key] = float('inf')
            return cache[key]

        length = sum(
            math.hypot(
                path.poses[i+1].pose.position.x - path.poses[i].pose.position.x,
                path.poses[i+1].pose.position.y - path.poses[i].pose.position.y
            )
            for i in range(len(path.poses)-1)
        )

        cache[key] = length
        return length

    pts = [all_points[i] for i in indices]
    n = len(pts)

    cost = [[dist(pts[i], pts[j]) if i!=j else 0 for j in range(n)] for i in range(n)]

    print("\n===== COST MATRIX =====")
    for i, row in enumerate(cost):
        print(f"{i}:", ["INF" if x == float('inf') else round(x,1) for x in row])

    best, best_cost = None, float('inf')

    for perm in itertools.permutations(range(1, n)):
        route = [0] + list(perm) + [0]
        total = sum(cost[route[i]][route[i+1]] for i in range(len(route)-1))

        if total < best_cost:
            best_cost, best = total, route

    print("Best cost:", round(best_cost, 2))

    return [indices[i] for i in best]

def main():
    rclpy.init()
    nav = BasicNavigator()

    nav.waitUntilNav2Active()

    # map index → pre-point
    pre_map = {
        2: (5.0, 11.0, 0),
        3: (5.0, 4.8, 0),
        10: (-4.5, 4.8, -math.pi),
        11: (-4.5, 10.5, -math.pi),
    }

    all_points = [
        (0.8, 0.8, 0), #0 điểm xuất phát
        (8.0, 14.5, -math.pi/2), #1
        (10.5, 10.5, -math.pi), #2
        (10.5, 5.5, -math.pi), #3
        (8.5, -7.5, -math.pi), #4
        (8.5, -22.0, -math.pi), #5
        (5.0, -28.0, math.pi/2), #6
        (-8.2, -29.0, 0), #7
        (-8.5, -17.0, 0), #8
        (-8.5, -3.5, 0), #9
        (-10.0, 4.8, 0), #10
        (-9.4, 11.15, 0), #11
        (-8.0, 15.0, -math.pi/2), #12
        (1.2, -4.0, math.pi/2), #13
        (2.0, -11.0, math.pi/2), #14
        (2.0, -19.5, math.pi/2), #15
        (-2.8, -17.5, math.pi/2), #16
        (-2.0, -11.0, math.pi/2), #17
        (-1.2, -4.0, math.pi/2) #18
    ]

    #selected_indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 0]
    #selected_indices = [10, 11, 12, 0]
    selected_indices = []

    print("Nhập các phòng (1 -> 18), nhập 'q' để kết thúc:")
    while True:
        user_input = input("Phòng: ")
        if user_input.lower() == 'q':
            break
        try:
            room = int(user_input)
            if not (1 <= room <= 18):
                print("❌ Chỉ được nhập từ 1 đến 18!")
                continue
            if room in selected_indices:
                print("⚠️ Phòng đã được chọn, không được nhập trùng!")
                continue
            selected_indices.append(room)
        except ValueError:
            print("❌ Vui lòng nhập số hợp lệ!")
    print("Danh sách phòng đã chọn:", selected_indices)


    optimized_path = optimize_path(nav, all_points, selected_indices)

    print("Selected indices:", selected_indices)
    print("--> Optimized Route:", optimized_path)

    for idx, i in enumerate(optimized_path):

        # 👉 chỉ skip phần tử đầu tiên nếu là Home
        if idx == 0 and i == 0:
            continue

        if i in pre_map:
            go(nav, *pre_map[i], all_points[0][0], all_points[0][1])

        go(nav, *all_points[i], all_points[0][0], all_points[0][1])

        if i in pre_map:
            go(nav, *pre_map[i], all_points[0][0], all_points[0][1])

    rclpy.shutdown()


if __name__ == '__main__':
    main()