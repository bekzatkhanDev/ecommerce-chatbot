"use client";

import { ProductGrid } from "@/components/products/ProductGrid";
import { Button } from "@/components/ui/button";
import { PixelAnimation } from "@/components/ui/PixelAnimation";
import api from "@/lib/api";
import { Product } from "@/types";
import { ArrowRight, Sprout, ShoppingBag } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function HomePage() {
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFeaturedProducts();
  }, []);

  const fetchFeaturedProducts = async () => {
    try {
      const response = await api.get("/products/", {
        params: { limit: 8, min_rating: 4.5 },
      });
      if (response.data.success) {
        setFeaturedProducts(response.data.products);
      }
    } catch (error) {
      console.error("Failed to fetch featured products:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="relative py-20 px-4 text-center overflow-hidden">
        <PixelAnimation className="z-0" opacity={1} speed={1} />
        <div className="absolute inset-0 bg-gradient-radial from-green-900 via-green-900/40 to-transparent z-5"></div>
        <div className="container max-w-4xl relative z-10">
          <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-green-400 to-green-300 bg-clip-text text-transparent">
            Fresh from Local Farms
          </h1>
          <p className="text-xl text-foreground mb-8 max-w-2xl mx-auto">
            Discover farm-fresh products delivered straight to your table. Support
            local farmers and enjoy the finest organic, seasonal, and sustainably
            grown food.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" asChild className="bg-green-600 hover:bg-green-700">
              <Link href="/products">
                <ShoppingBag className="mr-2 h-5 w-5" />
                Shop Fresh Products
              </Link>
            </Button>
            <Button size="lg" variant="outline" asChild>
              <Link href="/farms">
                <Sprout className="mr-2 h-5 w-5" />
                Meet Our Farmers
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="container px-4">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-3xl font-bold mb-2">Seasonal Favorites</h2>
            <p className="text-muted-foreground">
              Hand-picked selection of the freshest seasonal produce and farm goods
            </p>
          </div>
          <Button variant="outline" asChild>
            <Link href="/products">
              View All
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </div>

        <ProductGrid products={featuredProducts} loading={loading} />
      </section>

      {/* Why Choose Us Section */}
      <section className="container px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">Why Choose Farm Fresh?</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Experience the difference of truly fresh, locally sourced food
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center p-6 rounded-lg border bg-card">
            <div className="mx-auto h-12 w-12 rounded-full bg-green-100 flex items-center justify-center mb-4">
              <Sprout className="h-6 w-6 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Farm to Table</h3>
            <p className="text-muted-foreground">
              Direct from local farms to your doorstep, ensuring maximum freshness
              and flavor
            </p>
          </div>

          <div className="text-center p-6 rounded-lg border bg-card">
            <div className="mx-auto h-12 w-12 rounded-full bg-green-100 flex items-center justify-center mb-4">
              <svg
                className="h-6 w-6 text-green-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">Certified Organic</h3>
            <p className="text-muted-foreground">
              All our organic products are certified, ensuring no harmful pesticides
              or chemicals
            </p>
          </div>

          <div className="text-center p-6 rounded-lg border bg-card">
            <div className="mx-auto h-12 w-12 rounded-full bg-green-100 flex items-center justify-center mb-4">
              <svg
                className="h-6 w-6 text-green-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-2">Support Local</h3>
            <p className="text-muted-foreground">
              Every purchase supports local farmers and sustainable agriculture
              practices
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-background py-16 relative overflow-hidden">
        <PixelAnimation className="z-0" opacity={1} speed={1} />
        <div className="absolute inset-0 bg-gradient-radial from-green-900 via-green-900/30 to-transparent z-5"></div>
        <div className="container px-4 text-center relative z-10">
          <h2 className="text-3xl font-bold mb-4">Ready to Eat Fresh?</h2>
          <p className="text-foreground mb-8 max-w-2xl mx-auto">
            Join thousands of customers who trust us for their farm-fresh food needs
          </p>
          <Button size="lg" asChild className="bg-green-600 hover:bg-green-700">
            <Link href="/products">
              <ShoppingBag className="h-5 w-5" />
              Start Shopping
            </Link>
          </Button>
        </div>
      </section>
    </div>
  );
}