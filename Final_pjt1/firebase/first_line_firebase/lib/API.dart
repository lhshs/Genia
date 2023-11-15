import 'dart:convert';
import 'package:http/http.dart' as http;

Future<Map<String, dynamic>> getFastAPIResponse(uniqueFileName) async {
  print('<<<<<<<<<<<<<<<< unique print >>>>>>>>>>>>>>>');
  print(uniqueFileName);
  print('http://52.78.70.58:8000/predict?img_name=$uniqueFileName');
  final response = await http.get(Uri.parse('http://52.78.70.58:8000/predict?img_name=$uniqueFileName'));
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
