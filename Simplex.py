import numpy as np

class SimplexTable:
    def __init__(self, v_cnt, e_cnt, s_cnt, obj, e_left, e_right, e_compare):
        self.v_cnt = v_cnt  # 変数の数
        self.e_cnt = e_cnt  # 制約の数
        self.s_cnt = s_cnt  # スラック変数の数
        self.table = np.zeros((e_cnt + 1, v_cnt + s_cnt + 1))  # 単体表
        self.v_idx = np.zeros(e_cnt, dtype=int)  # 基底変数のインデックス
        self.obj = obj  # 目的関数の係数

        # 制約の係数を表に設定
        for i in range(e_cnt):
            self.table[i, :v_cnt] = e_left[i]  # 制約式の左辺の係数
            self.table[i, v_cnt + i] = 1  # スラック変数を追加
            self.table[i, -1] = e_right[i]  # 右辺の値を設定

    def initialize_objective(self):
        # 目的関数行（z行）の初期化
        for j in range(self.v_cnt + self.s_cnt + 1):
            self.table[self.e_cnt][j] = 0.0

        # 目的関数の係数を設定
        for j in range(1, self.v_cnt + 1):
            self.table[self.e_cnt][j] = -self.obj[j - 1]
        print(self.table)

    def display(self):
        print("Simplex Table:")
        print(self.table)

    def Pivot(self):
        min_ratio = float('inf')
        pivot_row = -1
        pivot_col = -1

        # 最小コスト列（ピボット列）の選択
        for i in range(self.v_cnt + self.s_cnt + 1):
            if self.table[self.e_cnt][i] < 0:  # ピボット列候補
                for j in range(self.e_cnt):
                    if self.table[j][i] > 0:  # ゼロ除算を避ける
                        ratio = self.table[j][-1] / self.table[j][i]
                        if ratio < min_ratio:
                            min_ratio = ratio
                            pivot_row = j
                            pivot_col = i

        # ピボットが選ばれている場合に操作を実行
        if pivot_row != -1 and pivot_col != -1:
            self.apply_pivot(pivot_row, pivot_col)
            return True  # ピボット成功
        return False  # 最適解に到達

    def apply_pivot(self, row, col):
        # ピボット行を1にする
        self.table[row] /= self.table[row][col]
        # 他の行の更新
        for i in range(len(self.table)):
            if i != row:
                self.table[i] -= self.table[i][col] * self.table[row]

    def optimize(self):
        self.initialize_objective()  # 目的関数の初期化
        iteration = 0
        while any(self.table[self.e_cnt, j] < 0 for j in range(self.v_cnt + self.s_cnt)):
            print(f"Iteration {iteration}:")
            self.display()
            if not self.Pivot():
                print("最適解が得られました。")
                break
            iteration += 1
        print("最適解に到達しました。")
        self.display()
        return self.table[self.e_cnt, -1]  # 最適な目的関数の値を返す

# 目的関数の係数
obj = [5, 4]

# 制約式の係数と右辺
e_left = [[1.5, 3], [3, 1]]
e_right = [13.5, 10]

# 制約の比較（ここではすべて "Less" を仮定）
e_compare = ['Less', 'Less']

# スラック変数の数
s_cnt = 2

# シンプレックス表の初期化
simplex_table = SimplexTable(v_cnt=2, e_cnt=2, s_cnt=s_cnt, obj=obj, e_left=e_left, e_right=e_right, e_compare=e_compare)
simplex_table.display()
# 最適化の実行
optimal_value = simplex_table.optimize()
print("最適な目的関数の値:", optimal_value)
