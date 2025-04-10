import 'dart:async';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(CompanioApp());
}

class CompanioApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'COMPANIO',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primaryColor: Colors.black,
        scaffoldBackgroundColor: Colors.black,
        fontFamily: 'Arial',
        textTheme: TextTheme(
          bodyLarge: TextStyle(fontSize: 20, color: Colors.white),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.blueAccent,
            foregroundColor: Colors.white,
            padding: EdgeInsets.symmetric(horizontal: 30, vertical: 15),
            textStyle: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
            elevation: 10,
            shadowColor: Colors.blueAccent,
          ),
        ),
      ),
      home: SplashScreen(),
    );
  }
}

// Splash Screen with animation
class SplashScreen extends StatefulWidget {
  @override
  _SplashScreenState createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _fadeIn;
  late Animation<double> _scale;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
        vsync: this, duration: Duration(milliseconds: 2000));
    _fadeIn = CurvedAnimation(parent: _controller, curve: Curves.easeIn);
    _scale = Tween<double>(begin: 0.8, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.elasticOut),
    );
    _controller.forward();

    Timer(Duration(seconds: 4), () {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => LanguageScreen()),
      );
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: FadeTransition(
        opacity: _fadeIn,
        child: Center(
          child: ScaleTransition(
            scale: _scale,
            child: Text(
              'COMPANIO',
              style: TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: Colors.blueAccent,
                letterSpacing: 2,
              ),
            ),
          ),
        ),
      ),
    );
  }
}

// Language Selection Page
class LanguageScreen extends StatelessWidget {
  final String baseUrl = 'http://192.168.0.106:5000'; // Flask server

  Future<void> callFlaskEndpoint(String lang, BuildContext context) async {
    final String url = '$baseUrl/run/$lang';

    try {
      final response = await http.get(Uri.parse(url));
      if (response.statusCode == 200) {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => SuccessPage(lang: lang),
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Failed to start $lang assistant")),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Connection error! Is Flask running?")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Colors.black, Colors.blueGrey],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                "Choose Language",
                style: TextStyle(
                  fontSize: 24,
                  color: Colors.white,
                  letterSpacing: 1.5,
                ),
              ),
              SizedBox(height: 40),
              ElevatedButton.icon(
                onPressed: () => callFlaskEndpoint("tamil", context),
                icon: Icon(Icons.language),
                label: Text('Tamil'),
              ),
              SizedBox(height: 20),
              ElevatedButton.icon(
                onPressed: () => callFlaskEndpoint("english", context),
                icon: Icon(Icons.language),
                label: Text('English'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// Success Page
class SuccessPage extends StatelessWidget {
  final String lang;

  const SuccessPage({Key? key, required this.lang}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    String displayLang = lang[0].toUpperCase() + lang.substring(1);

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.blueAccent,
        title: Text('$displayLang Assistant'),
      ),
      body: Center(
        child: Text(
          '$displayLang assistant started!',
          style: TextStyle(
            fontSize: 22,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
      ),
    );
  }
}
