import React from 'react';
import { ArrowRight, Shield, Heart, Users, CheckCircle, Star, Clock, Globe } from 'lucide-react';
import { Link } from 'react-router-dom';

const Home = () => {
  const testimonials = [
    {
      name: "Sarah Johnson",
      role: "Small Business Owner",
      content: "InsureGuard has been a game-changer for my business. Their comprehensive coverage and excellent support give me peace of mind.",
      image: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&auto=format&fit=crop&w=128&h=128&q=80"
    },
    {
      name: "Michael Chen",
      role: "Family Protection",
      content: "The family insurance plans are exactly what we needed. The process was simple, and the coverage is excellent.",
      image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&auto=format&fit=crop&w=128&h=128&q=80"
    },
    {
      name: "Emily Rodriguez",
      role: "Healthcare Professional",
      content: "As someone in healthcare, I appreciate the attention to detail in their medical coverage. Truly outstanding service.",
      image: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixlib=rb-1.2.1&auto=format&fit=crop&w=128&h=128&q=80"
    }
  ];

  return (
    <div className="relative">
      {/* Hero Section with Background Image */}
      <div className="relative min-h-[800px] overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-pastel-blue via-white to-pastel-pink opacity-90" />
        <div className="absolute inset-0" style={{
          backgroundImage: "url('https://images.unsplash.com/photo-1557804506-669a67965ba0?ixlib=rb-1.2.1&auto=format&fit=crop&w=2000&q=80')",
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          opacity: '0.1'
        }} />
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-24">
          <div className="text-center">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-white shadow-md mb-8">
              <Star className="h-5 w-5 text-yellow-400" />
              <span className="ml-2 text-sm font-medium text-gray-600">Trusted by 10,000+ customers</span>
            </div>
            
            <h1 className="text-6xl md:text-7xl font-bold text-gray-900 mb-8 leading-tight">
              Protect What{' '}
              <span className="relative">
                <span className="relative z-10 text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
                  Matters Most
                </span>
                <span className="absolute bottom-0 left-0 w-full h-3 bg-pastel-yellow opacity-50 -rotate-2" />
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl mb-12 text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Experience peace of mind with our AI-powered insurance solutions, 
              tailored perfectly to protect you and your loved ones.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-6 justify-center">
              <Link
                to="/plans"
                className="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-full text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-200 shadow-lg"
              >
                Explore Plans <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link
                to="/compare"
                className="inline-flex items-center px-8 py-4 border-2 border-blue-600 text-lg font-medium rounded-full text-blue-600 hover:bg-blue-50 transform hover:scale-105 transition-all duration-200"
              >
                Compare Plans
              </Link>
            </div>
          </div>
        </div>

        {/* Floating Stats with Gradient Borders */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mb-32 relative z-10">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { icon: Shield, title: "10K+", subtitle: "Active Customers", color: "from-blue-400 to-blue-600" },
              { icon: Heart, title: "98%", subtitle: "Satisfaction Rate", color: "from-pink-400 to-purple-600" },
              { icon: Clock, title: "24/7", subtitle: "Expert Support", color: "from-green-400 to-teal-600" }
            ].map((stat, index) => (
              <div key={index} className="relative group">
                <div className="absolute -inset-0.5 bg-gradient-to-r from-pastel-blue to-pastel-purple rounded-2xl blur opacity-75 group-hover:opacity-100 transition duration-200" />
                <div className="relative bg-white rounded-xl p-8 flex items-center space-x-4 transform hover:-translate-y-1 transition-all duration-200">
                  <div className={`flex items-center justify-center w-12 h-12 rounded-full bg-gradient-to-r ${stat.color}`}>
                    <stat.icon className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-gray-900">{stat.title}</p>
                    <p className="text-gray-600">{stat.subtitle}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Features Section with Interactive Cards */}
      <div className="pt-48 pb-32 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-20">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Why Choose{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
                InsureGuard
              </span>
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              We combine cutting-edge technology with human expertise to deliver 
              the best insurance experience possible.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-12 sm:grid-cols-2 lg:grid-cols-3">
            {[
              {
                icon: Shield,
                title: 'Smart Coverage',
                description: 'AI-powered analysis ensures you get exactly the coverage you need, nothing more, nothing less.',
                color: 'from-blue-400 to-blue-600'
              },
              {
                icon: Heart,
                title: 'Family First',
                description: 'Specially designed plans that grow and adapt with your family\'s changing needs.',
                color: 'from-pink-400 to-purple-600'
              },
              {
                icon: Globe,
                title: 'Global Protection',
                description: 'Coverage that travels with you, providing protection wherever life takes you.',
                color: 'from-green-400 to-teal-600'
              }
            ].map((feature, index) => (
              <div key={index} className="relative group cursor-pointer">
                <div className="absolute -inset-4 bg-gradient-to-r from-pastel-blue to-pastel-pink rounded-xl blur opacity-0 group-hover:opacity-75 transition duration-200" />
                <div className="relative bg-white rounded-xl shadow-lg p-8 transform group-hover:-translate-y-1 transition-all duration-200">
                  <div className={`flex items-center justify-center w-14 h-14 rounded-full bg-gradient-to-r ${feature.color} mb-6`}>
                    <feature.icon className="h-7 w-7 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">{feature.title}</h3>
                  <p className="text-gray-600 leading-relaxed">{feature.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Testimonials Section */}
      <div className="py-24 bg-gradient-to-br from-pastel-blue/10 to-pastel-purple/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Trusted by Thousands</h2>
            <p className="text-xl text-gray-600">Hear what our satisfied customers have to say</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="bg-white rounded-xl shadow-lg p-8 relative">
                <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-pastel-blue to-pastel-purple opacity-10 rounded-bl-full" />
                <img
                  src={testimonial.image}
                  alt={testimonial.name}
                  className="w-16 h-16 rounded-full mb-6 border-4 border-white shadow-lg"
                />
                <p className="text-gray-600 mb-6 italic">"{testimonial.content}"</p>
                <div>
                  <p className="font-semibold text-gray-900">{testimonial.name}</p>
                  <p className="text-sm text-gray-500">{testimonial.role}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="relative overflow-hidden rounded-3xl">
            <div className="absolute inset-0 bg-gradient-to-r from-pastel-blue to-pastel-purple opacity-90" />
            <div className="absolute inset-0" style={{
              backgroundImage: "url('https://images.unsplash.com/photo-1557804506-669a67965ba0?ixlib=rb-1.2.1&auto=format&fit=crop&w=2000&q=80')",
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              opacity: '0.1'
            }} />
            
            <div className="relative px-8 py-16 md:px-16 md:py-20 text-center">
              <h2 className="text-4xl font-bold text-white mb-6">
                Ready to Secure Your Future?
              </h2>
              <p className="text-xl text-white/90 mb-10 max-w-2xl mx-auto">
                Join thousands of satisfied customers who trust InsureGuard with their protection needs.
                Get started today and experience the difference.
              </p>
              <Link
                to="/signup"
                className="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-full text-blue-600 bg-white hover:bg-gray-50 transform hover:scale-105 transition-all duration-200 shadow-lg"
              >
                Get Protected Today <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;