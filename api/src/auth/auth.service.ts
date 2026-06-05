import { Injectable } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class AuthService {
  constructor(private prisma: PrismaService, private jwt: JwtService) {}

  async loginConGoogle(googleSub: string, email: string) {
    let user = await this.prisma.user.findUnique({ where: { email } });
    if (!user) {
      user = await this.prisma.user.create({ data: { email, googleSub } });
    } else if (!user.googleSub) {
      user = await this.prisma.user.update({ where: { id: user.id }, data: { googleSub } });
    }
    const token = await this.jwt.signAsync(
      { sub: user.id, email: user.email },
      { secret: process.env.JWT_SECRET || 'dev-secret', expiresIn: '30d' },
    );
    return { token, user };
  }
}
