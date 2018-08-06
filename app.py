from flask import Flask, request, render_template_string, json

app = Flask(__name__)

template = """
<html>
<head>
    <title>Json to Dart classes - Online converter</title>
    <meta name="description" content="JSON to dart classes online converters">
    <meta name="keywords" content="Json2dart,Json To Dart">
    <meta name="author" content="J2D Team">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
          integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
</head>
<body> 
    <header>
        <div class="navbar navbar-dark bg-dark box-shadow">
            <div class="container-fluid d-flex justify-content-between">
                <a href="#" class="navbar-brand d-flex align-items-center">
                    <strong>Json to Dart</strong>
                </a>
            </div>
        </div>
    </header>
    <main role="main">
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">JSON Here</h5>
                        <p class="card-text">
                        <form method="POST" action="">
                            <textarea name="json_data" style="width:100%;height:500px;">{{ json }}</textarea>
                            <button id="submit" class="btn btn-primary" style="margin-top:5px;">Convert</button>
                        </form>
                        </p>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">Result</h5>
                            <p class="card-text">
                            <pre style="width:100%;height:540px;background:#eee;">
                                {{ dart }}
                            </pre>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main> 
    <footer class="container-fluid text-muted">
        <p>(C) 2018 Json to Dart, Hope you enjoy!</p>
    </footer> 
</body>
<html>
"""

sample = {
    "username": "sin.sarath@gmail.com",
    "password": "fuckingPassowrd"
}


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        json_data = request.values.get('json_data')  # Your form's
        data = json.loads(json_data)
        dart = to_dart(data)
        return render_template_string(template,
                                      json=json_data,
                                      dart=dart)
    else:
        data = json.dumps(sample)
        dart = ""
        return render_template_string(template,
                                      json=data,
                                      dart=dart)


def to_dart(data):
    if not isinstance(data, dict):
        return 'Not support!'
    dart_template = \
        """
        class {{class_name}} {
          {% for f in fields %}
          {{f.datatype }} {{ f.name }};
          {% endfor %} 
        
          {{class_name}}({
            {% for f in fields -%}
            this.{{f.name}},
            {%- endfor %}
          });
          
          factory {{class_name}}.fromJson(Map<String,dynamic> json){
            return {{class_name}}(
            {% for f in fields %}
            {{f.name}}: json['{{f.name}}'],
            {% endfor %}
            );
          }
          
          Map<String, dynamic> toJson() => {
            {% for f in fields %} 
            '{{f.name}}': {{f.name}},
            {% endfor %}
          };
        }
        """
    '''
    class {{class_name}} {
          {% for f in fields %}
          {{ f.name }} {{f.type }};
          {% endfor %}
          String id;
          String name;
          String full_name;
        
          {{class_name}}({
            {% for f in fields %}
            this.{{f.name}},
            {% endfor %}
          });
          
          factory {{class_name}}.fromJson(Map<String,dynamic> json){
            return {{class_name}}(
            {% for f in fields %}
            {{f.name}}: json['{{f.name}}'],
            {% endfor %}
            );
          }
        
          Map<String, dynamic> toJson() => {

            'avatarUrl': name,
            'name': full_name,
            {% for f in fields %}
            {: json['{{f.name}}'],
            '{k}': id,
            {% endfor %}
          };
        }
        '''
    class_name = 'RootObject'
    fields = []  # [{'name': 'username', 'datatype': 'String'}]

    for k, v in data.iteritems():
        fields.append({
            'name': k,
            'datatype': 'String'
        })
    return render_template_string(dart_template, class_name=class_name, fields=fields)


if __name__ == '__main__':
    app.debug = True
    app.usereloader = True
    app.run()
