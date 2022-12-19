import imagematrix


class ResizeableImage(imagematrix.ImageMatrix):

    #non dp method for seam (inefficient)
    def non_dp(self, i, j):
        w = self.width

        # edge cases
        if j == 0:
            return self.energy(i, j)
        elif i == 0:
            return min(self.non_dp(i, j - 1), self.non_dp(i + 1, j - 1)) + self.energy(
                i, j
            )
        elif i == w - 1:
            return min(self.non_dp(i, j - 1), self.non_dp(i - 1, j - 1)) + self.energy(
                i, j
            )
        # normal case
        else:
            return min(
                self.non_dp(i - 1, j - 1),
                self.non_dp(i, j - 1),
                self.non_dp(i + 1, j - 1),
            ) + self.energy(i, j)

    #still required to cache energy results, required for non dp method
    def non_dp_table(self):
        h, w = self.height, self.width
        E = [[self.non_dp(i, j) for i in range(w)] for j in range(h)]
        return E

    #creates min energy table that includes every point, required for dp method
    def make_table(self):
        h, w = self.height, self.width
        E = [[self.energy(i, j) for i in range(w)] for j in range(h)]
        for i in range(1, h):
            # edge cases
            E[i][0] += min(E[i - 1][0], E[i - 1][1])
            E[i][w - 1] += min(E[i - 1][w - 1], E[i - 1][w - 2])

            # normal case
            for j in range(1, w - 1):
                E[i][j] += min(E[i - 1][j - 1], E[i - 1][j], E[i - 1][j + 1])

        return E

    #effectively the trace back function
    def find_path(self, dp=True):
        
        if (self.height == 1 and self.width == 1):
            return [(0,0)]
        

        h, w = self.height, self.width
        if dp:
            table = self.make_table()
        else:
            table = self.non_dp_table()
        S = [None for s in range(h)]
        last_row = table[h - 1]
        i = last_row.index(min(last_row))
        temp1 = i
        for j in range(h - 1, -1, -1):
            # case in which the cell is not an edge
            if (i != 0) and (i != w - 1):
                x = table[j - 1][i - 1]
                y = table[j - 1][i]
                z = table[j - 1][i + 1]
                if (x < y) and (x < z):
                    S[j - 1] = i - 1
                    i = i - 1
                elif y < z:
                    S[j - 1] = i
                else:
                    S[j - 1] = i + 1
                    i = i + 1
            # case for left edge
            elif i == 0:
                if table[j - 1][0] <= table[j - 1][1]:
                    S[j - 1] = 0
                    i = 0
                else:
                    S[j - 1] = 1
                    i = 1
            # case for right edge / choosing one path if equal
            else:
                if table[j - 1][w - 1] <= table[j - 1][w - 2]:
                    S[j - 1] = w - 1
                    i = w - 1
                else:
                    S[j - 1] = w - 2
                    i = w - 2
        # S holds column numbers, enumerate with row numbers
        S[h - 1] = temp1
        for a in range(len(S)):
            temp = S[a]
            S[a] = (temp, a)
        return S

    def best_seam(self, dp=True):
        return self.find_path(dp)

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
