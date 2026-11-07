import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'Trang1.dart';
import 'Trang2.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Chào UEH',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        scaffoldBackgroundColor: const Color(0xFFF5F4F9),
      ),
      home: const TrangChu(),
    );
  }
}

class TrangChu extends StatefulWidget {
  const TrangChu({super.key});

  @override
  State<TrangChu> createState() => _TrangChuState();
}

class _TrangChuState extends State<TrangChu> {
  int _selectedIndex = 0;

  static const _pages = [Trang1(), Trang2()];
  static const _destinations = [
    (Icons.home_filled, Icons.home_outlined, 'Trang chủ'),
    (Icons.calendar_month, Icons.calendar_month_outlined, 'Lịch công tác'),
    (
      Icons.notifications_active,
      Icons.notifications_none_outlined,
      'Thông báo',
    ),
    (Icons.person, Icons.person_outline, 'Cá nhân'),
  ];

  void _onDestinationSelected(int index) {
    if (index >= _pages.length) {
      ScaffoldMessenger.of(context)
        ..hideCurrentSnackBar()
        ..showSnackBar(
          const SnackBar(
            content: Text('Chức năng đang được cập nhật.'),
            duration: Duration(seconds: 2),
          ),
        );
      return;
    }

    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return AnnotatedRegion<SystemUiOverlayStyle>(
      value: const SystemUiOverlayStyle(
        statusBarColor: Color(0xFFB32D36),
        statusBarIconBrightness: Brightness.light,
        systemNavigationBarColor: Colors.white,
        systemNavigationBarIconBrightness: Brightness.dark,
      ),
      child: Scaffold(
        body: IndexedStack(index: _selectedIndex, children: _pages),
        bottomNavigationBar: BottomNavigationBar(
          currentIndex: _selectedIndex,
          onTap: _onDestinationSelected,
          type: BottomNavigationBarType.fixed,
          backgroundColor: Colors.white,
          elevation: 8,
          selectedItemColor: const Color(0xFFB32D36),
          unselectedItemColor: const Color(0xFF4F5663),
          selectedFontSize: 13,
          unselectedFontSize: 13,
          items: [
            for (var index = 0; index < _destinations.length; index++)
              BottomNavigationBarItem(
                icon: Icon(_destinations[index].$2),
                activeIcon: Icon(_destinations[index].$1),
                label: _destinations[index].$3,
              ),
          ],
        ),
      ),
    );
  }
}
