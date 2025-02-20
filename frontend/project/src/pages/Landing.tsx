import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, Heart, Users, Trophy } from 'lucide-react';

export function Landing() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-pastel-blue to-white">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto">
          <div className="relative z-10 pb-8 sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
            <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
              <div className="sm:text-center lg:text-left">
                <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                  <span className="block">Find the perfect</span>
                  <span className="block text-primary-600">health insurance plan</span>
                </h1>
                <p className="mt-3 text-base text-gray-600 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                  Let our AI-powered platform help you discover the best health insurance plans tailored to your needs. Get personalized recommendations in minutes.
                </p>
                <div className="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                  <div className="rounded-md shadow">
                    <Link
                      to="/login"
                      className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-500 hover:bg-primary-600 md:py-4 md:text-lg md:px-10"
                    >
                      Get Started
                    </Link>
                  </div>
                  <div className="mt-3 sm:mt-0 sm:ml-3">
                    <Link
                      to="/compare"
                      className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-primary-700 bg-pastel-blue hover:bg-primary-100 md:py-4 md:text-lg md:px-10"
                    >
                      Compare Plans
                    </Link>
                  </div>
                </div>
              </div>
            </main>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:text-center">
            <h2 className="text-base text-primary-600 font-semibold tracking-wide uppercase">Features</h2>
            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              Why Choose HealthGuard AI?
            </p>
          </div>

          <div className="mt-10">
            <div className="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-4">
              <div className="flex flex-col items-center p-6 bg-pastel-pink bg-opacity-30 rounded-xl">
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                  <Shield className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-lg font-medium text-gray-900">Comprehensive Coverage</h3>
                <p className="mt-2 text-base text-gray-600 text-center">
                  Find plans that cover all your healthcare needs.
                </p>
              </div>

              <div className="flex flex-col items-center p-6 bg-pastel-purple bg-opacity-30 rounded-xl">
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                  <Heart className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-lg font-medium text-gray-900">Personalized Care</h3>
                <p className="mt-2 text-base text-gray-600 text-center">
                  Get recommendations tailored to your health profile.
                </p>
              </div>

              <div className="flex flex-col items-center p-6 bg-pastel-green bg-opacity-30 rounded-xl">
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                  <Users className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-lg font-medium text-gray-900">Family Plans</h3>
                <p className="mt-2 text-base text-gray-600 text-center">
                  Coverage options for the whole family.
                </p>
              </div>

              <div className="flex flex-col items-center p-6 bg-pastel-yellow bg-opacity-30 rounded-xl">
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white">
                  <Trophy className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-lg font-medium text-gray-900">Best Value</h3>
                <p className="mt-2 text-base text-gray-600 text-center">
                  Find plans that fit your budget without compromising quality.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}