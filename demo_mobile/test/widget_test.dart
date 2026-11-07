import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:demo_mobile/main.dart';

void main() {
  testWidgets('bottom navigation switches between Trang1 and Trang2', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(const MyApp());

    expect(find.text('Không tìm thấy lịch cá nhân'), findsOneWidget);

    final bottomNavigationBar = find.byType(BottomNavigationBar);
    await tester.tap(
      find.descendant(
        of: bottomNavigationBar,
        matching: find.text('Lịch công tác'),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Chưa có lịch công tác hôm nay'), findsOneWidget);
    expect(find.text('Lịch công tác sắp tới'), findsOneWidget);

    await tester.tap(
      find.descendant(
        of: bottomNavigationBar,
        matching: find.text('Trang chủ'),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Không tìm thấy lịch cá nhân'), findsOneWidget);
  });

  testWidgets('unfinished bottom destinations show an update message', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(const MyApp());

    final bottomNavigationBar = find.byType(BottomNavigationBar);
    await tester.tap(
      find.descendant(
        of: bottomNavigationBar,
        matching: find.text('Thông báo'),
      ),
    );
    await tester.pump();

    expect(find.text('Chức năng đang được cập nhật.'), findsOneWidget);
    expect(find.text('Không tìm thấy lịch cá nhân'), findsOneWidget);
  });
}
