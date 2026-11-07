// ignore_for_file: file_names

import 'package:flutter/material.dart';

import 'widgets/trang_layout.dart';

class Trang2 extends StatelessWidget {
  const Trang2({super.key});

  @override
  Widget build(BuildContext context) {
    return TrangLayout(
      statusTitle: 'Lịch công tác:',
      statusMessage: 'Chưa có lịch công tác hôm nay',
      child: const _LichCongTac(),
    );
  }
}

class _LichCongTac extends StatelessWidget {
  const _LichCongTac();

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Container(
              width: 5,
              height: 34,
              decoration: BoxDecoration(
                color: const Color(0xFF1689E8),
                borderRadius: BorderRadius.circular(8),
              ),
            ),
            const SizedBox(width: 12),
            const Text(
              'Lịch công tác',
              style: TextStyle(
                color: Color(0xFF222638),
                fontSize: 22,
                fontWeight: FontWeight.w700,
              ),
            ),
          ],
        ),
        const SizedBox(height: 18),
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(18),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
          ),
          child: const Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(Icons.calendar_today, color: Color(0xFF1689E8)),
                  SizedBox(width: 10),
                  Text(
                    'Lịch công tác sắp tới',
                    style: TextStyle(
                      color: Color(0xFF273044),
                      fontSize: 17,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ],
              ),
              SizedBox(height: 14),
              Text(
                'Hiện chưa có lịch công tác để hiển thị.',
                style: TextStyle(
                  color: Color(0xFF667085),
                  fontSize: 15,
                  height: 1.4,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
