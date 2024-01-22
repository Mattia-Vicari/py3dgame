#include <stdint.h>
#include <Python.h>

#define min(X, Y) (((X) < (Y)) ? (X) : (Y))
#define max(X, Y) (((X) > (Y)) ? (X) : (Y))

static void draw_triangle(uint8_t* buffer,
                          int bs_x, int bs_y, int bs_c,
                          float* depth_buffer,
                          int ds_x, int ds_y,
                          float p1xf, float p1yf, float p1z,
                          float p2xf, float p2yf, float p2z,
                          float p3xf, float p3yf, float p3z,
                          uint8_t R, uint8_t G, uint8_t B,
                          int w, int h) {

    const int p1x = (int) p1xf;
    const int p2x = (int) p2xf;
    const int p3x = (int) p3xf;
    const int p1y = (int) p1yf;
    const int p2y = (int) p2yf;
    const int p3y = (int) p3yf;

    const int min_x = max(min(min(p1x, p2x), p3x), 0);
    const int max_x = min(max(max(p1x, p2x), p3x), w - 1);
    const int min_y = max(min(min(p1y, p2y), p3y), 0);
    const int max_y = min(max(max(p1y, p2y), p3y), h - 1);

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

static void fill_bg(uint8_t* buffer,
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

PyDoc_STRVAR(ext_rendering__doc__,
"Low level drawing on the pygame buffer.");

PyDoc_STRVAR(draw_triangle__doc__,
"Draw a triangle on the pygame buffer.");

PyDoc_STRVAR(fill_bg__doc__,
"Fill the background with its color.");

static PyObject* py_draw_triangle(PyObject* self, PyObject* args)
{
    unsigned long long buffer_ptr;
    int bs_x, bs_y, bs_c;
    unsigned long long depth_buffer_ptr;
    int ds_x, ds_y;
    float p1xf, p1yf, p1z;
    float p2xf, p2yf, p2z;
    float p3xf, p3yf, p3z;
    uint8_t R, G, B;
    int w, h;

	if (!PyArg_ParseTuple(args, "KiiiKiifffffffffbbbii:draw_triangle",
                          &buffer_ptr, &bs_x, &bs_y, &bs_c,
                          &depth_buffer_ptr, &ds_x, &ds_y,
                          &p1xf, &p1yf, &p1z,
                          &p2xf, &p2yf, &p2z,
                          &p3xf, &p3yf, &p3z,
                          &R, &G, &B, &w, &h))
		return NULL;

    uint8_t* buffer = (uint8_t*) buffer_ptr;
    float* depth_buffer = (float*) depth_buffer_ptr;

	draw_triangle(buffer, bs_x, bs_y, bs_c,
                  depth_buffer, ds_x, ds_y,
                  p1xf, p1yf, p1z,
                  p2xf, p2yf, p2z,
                  p3xf, p3yf, p3z,
                  R, G, B, w, h);

	Py_RETURN_NONE;
}

static PyObject* py_fill_bg(PyObject* self, PyObject* args)
{
    unsigned long long buffer_ptr;
    int bs_x, bs_y, bs_c;
    uint8_t R, G, B;
    int w, h;

	if (!PyArg_ParseTuple(args, "Kiiibbbii:draw_triangle",
                          &buffer_ptr, &bs_x, &bs_y, &bs_c,
                          &R, &G, &B, &w, &h))
		return NULL;

    uint8_t* buffer = (uint8_t*) buffer_ptr;

	fill_bg(buffer, bs_x, bs_y, bs_c,
            R, G, B, w, h);

	Py_RETURN_NONE;
}

static PyMethodDef ext_rendering_methods[] = {
	{"draw_triangle",  py_draw_triangle, METH_VARARGS, draw_triangle__doc__},
    {"fill_bg",  py_fill_bg, METH_VARARGS, fill_bg__doc__},
	{NULL, NULL}
};

static struct PyModuleDef extRendering =
{
    PyModuleDef_HEAD_INIT,
    "ext_rendering",
    ext_rendering__doc__,
    -1,
    ext_rendering_methods
};

PyMODINIT_FUNC PyInit_ext_rendering(void)
{
    return PyModule_Create(&extRendering);
}