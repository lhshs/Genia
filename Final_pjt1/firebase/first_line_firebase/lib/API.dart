import 'dart:convert';
import 'package:http/http.dart' as http;

Future<Map<String, dynamic>> Yolo_API(uniqueFileName) async {
  print('<<<<<<<<<<<<<<<< YOLO API START >>>>>>>>>>>>>>>');
  print(uniqueFileName);
  print('http://3.38.61.144:8000/predict?img_name=$uniqueFileName');
  final response = await http.get(Uri.parse('http://3.38.61.144:8000/predict?img_name=$uniqueFileName'));
  final Map<String, dynamic> data = json.decode(response.body);
  // print(response.body);
  // print(response.body.runtimeType);
  // print(data);
  // print(data.runtimeType);
  // print(data['direction']);
  // print(data['number']);
  // print(data['action']);
  // print(data);

  return data;
}

Future<http.Response> Juuns_API(uniqueFileName) async {
  print('<<<<<<<<<<<<<<<< Juuns API START >>>>>>>>>>>>>>>');
  print(uniqueFileName);
  print('http://43.202.170.83:8000/predict?img_name=$uniqueFileName');
  final response = await http.get(Uri.parse('http://43.202.170.83:8000/predict?img_name=$uniqueFileName'));

  // print(response.body);
  // print(response.body.runtimeType);
  // print(data);
  // print(data.runtimeType);
  // print(data['direction']);
  // print(data['number']);
  // print(data['action']);
  // print(data);

  return response;
}
