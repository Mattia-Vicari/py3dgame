#include <stdint.h>
#include <algorithm>
#include <iostream>

extern "C" __declspec(dllexport) void draw_triangle(uint8_t* buffer,
                                                    int bs_x, int bs_y, int bs_c,
                                                    float* depth_buffer,
                                                    int ds_x, int ds_y,
                                                    float p1xf, float p1yf, float p1z,
                                                    float p2xf, float p2yf, float p2z,
                                                    float p3xf, float p3yf, float p3z,
                                                    uint8_t R, uint8_t G, uint8_t B,
                                                    int w, int h) {

    const int p1x = int(p1xf);
    const int p2x = int(p2xf);
    const int p3x = int(p3xf);
    const int p1y = int(p1yf);
    const int p2y = int(p2yf);
    const int p3y = int(p3yf);

    const int min_x = std::max(std::min(std::min(p1x, p2x), p3x), 0);
    const int max_x = std::min(std::max(std::max(p1x, p2x), p3x), w - 1);
    const int min_y = std::max(std::min(std::min(p1y, p2y), p3y), 0);
    const int max_y = std::min(std::max(std::max(p1y, p2y), p3y), h - 1);

    if (min_x > max_x + 1 || min_y > max_y + 1) return;

    const int p1_p2_x_diff = p1x - p2x;
    const int p2_p3_x_diff = p2x - p3x;
    const int p3_p1_x_diff = p3x - p1x;
    const int p1_p2_y_diff = p1y - p2y;
    const int p2_p3_y_diff = p2y - p3y;
    const int p3_p1_y_diff = p3y - p1y;
    const int p2_p1_cross = p1_p2_x_diff * p2y - p1_p2_y_diff * p2x;
    const int p3_p2_cross = p2_p3_x_diff * p3y - p2_p3_y_diff * p3x;
    const int p1_p3_cross = p3_p1_x_diff * p1y - p3_p1_y_diff * p1x;

    int area = p3_p1_y_diff * p2_p3_x_diff - p3_p1_x_diff * p2_p3_y_diff;

    if (area == 0) return;

    const float inv_area = 1.0f / area;

    float depth;
    int offset;
    int depth_offest;
    int s1;
    int s2;
    int s3;

    for (int y = min_y; y <= max_y; y++)
    {
        for (int x = min_x; x <= max_x; x++)
        {
            s1 = p1_p2_y_diff * x - p1_p2_x_diff * y + p2_p1_cross;
            s2 = p2_p3_y_diff * x - p2_p3_x_diff * y + p3_p2_cross;
            s3 = p3_p1_y_diff * x - p3_p1_x_diff * y + p1_p3_cross;

            if (((s1 > 0) && (s2 > 0) && (s3 > 0)) || ((s1 <= 0) && (s2 <= 0) && (s3 <= 0)))
            {
                depth = (p1z * s2 + p2z * s3 + p3z * s1) * inv_area;
                depth_offest = (x * ds_x + y * ds_y) / sizeof(float);

                if (depth < depth_buffer[depth_offest])
                {
                    offset = x * bs_x + y * bs_y;
                    buffer[offset] = R;
                    buffer[offset + bs_c] = G;
                    buffer[offset + bs_c + bs_c] = B;
                    depth_buffer[depth_offest] = depth;
                }
            }
        }
    }
}

extern "C" __declspec(dllexport) void fill_bg(uint8_t* buffer,
                                              int bs_x, int bs_y, int bs_c,
                                              uint8_t R, uint8_t G, uint8_t B,
                                              int w, int h) {
    for (int y = 0; y < h; y++)
    {
        for (int x = 0; x < w; x++)
        {
            int offset = x * bs_x + y * bs_y;
            buffer[offset] = R;
            buffer[offset + bs_c] = G;
            buffer[offset + bs_c + bs_c] = B;
        }
    }
}