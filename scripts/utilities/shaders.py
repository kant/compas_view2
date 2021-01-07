from OpenGL import GL


class Shader:

    def __init__(self, vertex, fragment):
        self.program = make_shader_program(vertex, fragment)
        self.locations = {}

    def uniform4x4(self, name, value):
        loc = GL.glGetUniformLocation(self.program, name)
        GL.glUniformMatrix4fv(loc, 1, True, value)

    def uniform1i(self, name, value):
        loc = GL.glGetUniformLocation(self.program, name)
        GL.glUniform1i(loc, value)

    def uniform1f(self, name, value):
        loc = GL.glGetUniformLocation(self.program, name)
        GL.glUniform1f(loc, value)

    def uniform3f(self, name, value):
        loc = GL.glGetUniformLocation(self.program, name)
        GL.glUniform3f(loc, *value)

    def bind(self):
        GL.glUseProgram(self.program)

    def release(self):
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glUseProgram(0)

    def enable_attribute(self, name):
        location = GL.glGetAttribLocation(self.program, name)
        GL.glEnableVertexAttribArray(location)
        self.locations[name] = location

    def bind_attribute(self, name, value):
        location = self.locations[name]
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, value)
        GL.glVertexAttribPointer(location, 3, GL.GL_FLOAT, False, 0, None)

    def disable_attribute(self, name):
        GL.glDisableVertexAttribArray(self.locations[name])
        del self.locations[name]

    def draw_triangles(self):
        # GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.front['elements'])
        # GL.glDrawElements(GL.GL_TRIANGLES, self.front['n'], GL.GL_UNSIGNED_INT, None)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, GL.GL_BUFFER_SIZE)

    def draw_lines(self):
        # GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.edges['elements'])
        # GL.glDrawElements(GL.GL_LINES, self.edges['n'], GL.GL_UNSIGNED_INT, None)
        GL.glDrawArrays(GL.GL_LINES, 0, GL.GL_BUFFER_SIZE)

    def draw_points(self, size=1):
        GL.glPointSize(size)
        # GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.vertices['elements'])
        # GL.glDrawElements(GL.GL_POINTS, self.vertices['n'], GL.GL_UNSIGNED_INT, None)
        GL.glDrawArrays(GL.GL_POINTS, 0, GL.GL_BUFFER_SIZE)


def make_shader_program(vsource, fsource):
    vertex = compile_vertex_shader(vsource)
    fragment = compile_fragment_shader(fsource)
    program = GL.glCreateProgram()
    GL.glAttachShader(program, vertex)
    GL.glAttachShader(program, fragment)
    GL.glLinkProgram(program)
    GL.glValidateProgram(program)
    result = GL.glGetProgramiv(program, GL.GL_LINK_STATUS)
    if not result:
        raise RuntimeError(GL.glGetProgramInfoLog(program))
    GL.glDeleteShader(vertex)
    GL.glDeleteShader(fragment)
    return program


def compile_vertex_shader(source):
    shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
    GL.glShaderSource(shader, source)
    GL.glCompileShader(shader)
    result = GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS)
    if not result:
        raise RuntimeError(GL.glGetShaderInfoLog(shader))
    return shader


def compile_fragment_shader(source):
    shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
    GL.glShaderSource(shader, source)
    GL.glCompileShader(shader)
    result = GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS)
    if not result:
        raise RuntimeError(GL.glGetShaderInfoLog(shader))
    return shader

