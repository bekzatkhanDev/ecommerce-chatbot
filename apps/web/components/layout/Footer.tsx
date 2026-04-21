import { Separator } from "@/components/ui/separator";
import Link from "next/link";

export function Footer() {
  return (
    <footer className="border-t bg-background flex-shrink-0">
      <div className="container py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-3">
            <div className="flex items-center space-x-0.5">
              <div className="h-6 w-6 rounded bg-primary flex items-center justify-center">
                <span className="text-primary-foreground font-bold text-xl">
                  S
                </span>
              </div>
              <span className="font-bold">TORE</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Свежие фермерские продукты с доставкой прямо к вашему столу с помощью ИИ-ассистента.
            </p>
          </div>

          <div className="space-y-3">
            <h4 className="text-sm font-semibold">Товары</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link
                  href="/products?category=Electronics"
                  className="hover:text-foreground"
                >
                  Овощи и фрукты
                </Link>
              </li>
              <li>
                <Link
                  href="/products?category=Smartphones"
                  className="hover:text-foreground"
                >
                  Молочные продукты
                </Link>
              </li>
              <li>
                <Link
                  href="/products?category=Laptops"
                  className="hover:text-foreground"
                >
                  Мясо и птица
                </Link>
              </li>
              <li>
                <Link
                  href="/products?category=Gaming"
                  className="hover:text-foreground"
                >
                  Сезонные товары
                </Link>
              </li>
            </ul>
          </div>

          <div className="space-y-3">
            <h4 className="text-sm font-semibold">Поддержка</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link href="/chat" className="hover:text-foreground">
                  ИИ Ассистент
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-foreground">
                  Центр помощи
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-foreground">
                  Связаться с нами
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-foreground">
                  Возврат товаров
                </Link>
              </li>
            </ul>
          </div>

          <div className="space-y-3">
            <h4 className="text-sm font-semibold">Компания</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link href="#" className="hover:text-foreground">
                  О нас
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-foreground">
                  Конфиденциальность
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-foreground">
                  Условия использования
                </Link>
              </li>
              <li>
                <Link href="#" className="hover:text-foreground">
                  Вакансии
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <Separator className="my-6" />

        <div className="flex flex-col sm:flex-row justify-between items-center text-sm text-muted-foreground">
          <p>&copy; 2024 S-TORE. Все права защищены.</p>
          <p>Создано на Next.js и Shadcn UI</p>
        </div>
      </div>
    </footer>
  );
}
